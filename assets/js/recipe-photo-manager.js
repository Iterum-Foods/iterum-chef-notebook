/**
 * Recipe Photo Manager
 * Upload, manage, and display recipe photos
 */

class RecipePhotoManager {
    constructor() {
        this.maxPhotos = 10;
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        console.log('📸 Recipe Photo Manager initialized');
    }
    
    /**
     * Upload photo(s) for a recipe
     */
    async uploadPhotos(recipeId, files) {
        const photos = [];
        
        for (const file of files) {
            // Validate file
            if (!this.validateFile(file)) {
                showWarning(`Skipped ${file.name}: Invalid file type or size`);
                continue;
            }
            
            try {
                // Convert to base64 for local storage
                const base64 = await this.fileToBase64(file);
                
                const photo = {
                    id: this.generatePhotoId(),
                    recipeId: recipeId,
                    fileName: file.name,
                    fileType: file.type,
                    fileSize: file.size,
                    data: base64,
                    uploadedAt: new Date().toISOString(),
                    uploadedBy: window.authManager?.currentUser?.email || 'unknown'
                };
                
                photos.push(photo);
                
                // Also try to upload to Firebase Storage if available
                if (window.firebase && window.firebase.storage) {
                    try {
                        await this.uploadToFirebase(photo, file);
                    } catch (error) {
                        console.warn('Firebase upload failed, using local storage only:', error);
                    }
                }
                
            } catch (error) {
                console.error('Error processing photo:', error);
                showError(`Failed to upload ${file.name}`);
            }
        }
        
        if (photos.length > 0) {
            // Save photos to recipe
            await this.savePhotosToRecipe(recipeId, photos);
            showSuccess(`${photos.length} photo(s) uploaded successfully!`);
        }
        
        return photos;
    }
    
    /**
     * Validate file
     */
    validateFile(file) {
        if (!this.allowedTypes.includes(file.type)) {
            showWarning(`${file.name}: Only JPEG, PNG, and WebP images are allowed`);
            return false;
        }
        
        if (file.size > this.maxFileSize) {
            showWarning(`${file.name}: File too large (max 5MB)`);
            return false;
        }
        
        return true;
    }
    
    /**
     * Convert file to base64
     */
    fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }
    
    /**
     * Generate unique photo ID
     */
    generatePhotoId() {
        return 'photo_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    /**
     * Upload to Firebase Storage
     */
    async uploadToFirebase(photo, file) {
        if (!window.firebase || !window.firebase.storage) {
            throw new Error('Firebase not available');
        }
        
        const storage = window.firebase.storage();
        const storageRef = storage.ref();
        const photoRef = storageRef.child(`recipe-photos/${photo.recipeId}/${photo.id}`);
        
        await photoRef.put(file);
        const downloadURL = await photoRef.getDownloadURL();
        
        photo.firebaseUrl = downloadURL;
        return downloadURL;
    }
    
    /**
     * Save photos to recipe
     */
    async savePhotosToRecipe(recipeId, newPhotos) {
        // Get existing recipe photos
        const existingPhotos = this.getRecipePhotos(recipeId);
        
        // Combine and limit to maxPhotos
        const allPhotos = [...existingPhotos, ...newPhotos].slice(0, this.maxPhotos);
        
        // Save to localStorage
        const photosKey = `recipe_photos_${recipeId}`;
        localStorage.setItem(photosKey, JSON.stringify(allPhotos));
        
        // Also update the recipe object if it exists
        if (window.universalRecipeManager) {
            const recipe = window.universalRecipeManager.getRecipe(recipeId);
            if (recipe) {
                recipe.photos = allPhotos;
                recipe.hasPhotos = allPhotos.length > 0;
                recipe.photoCount = allPhotos.length;
                window.universalRecipeManager.updateRecipe(recipeId, recipe);
            }
        }
        
        // Trigger event for UI updates
        window.dispatchEvent(new CustomEvent('recipePhotosUpdated', {
            detail: { recipeId, photos: allPhotos }
        }));
    }
    
    /**
     * Get all photos for a recipe
     */
    getRecipePhotos(recipeId) {
        const photosKey = `recipe_photos_${recipeId}`;
        const stored = localStorage.getItem(photosKey);
        return stored ? JSON.parse(stored) : [];
    }
    
    /**
     * Delete a photo
     */
    async deletePhoto(recipeId, photoId) {
        const photos = this.getRecipePhotos(recipeId);
        const filtered = photos.filter(p => p.id !== photoId);
        
        // Save updated list
        const photosKey = `recipe_photos_${recipeId}`;
        localStorage.setItem(photosKey, JSON.stringify(filtered));
        
        // Delete from Firebase if it exists
        if (window.firebase && window.firebase.storage) {
            try {
                const storage = window.firebase.storage();
                const photoRef = storage.ref().child(`recipe-photos/${recipeId}/${photoId}`);
                await photoRef.delete();
            } catch (error) {
                console.warn('Firebase delete failed:', error);
            }
        }
        
        showSuccess('Photo deleted');
        
        // Trigger event
        window.dispatchEvent(new CustomEvent('recipePhotosUpdated', {
            detail: { recipeId, photos: filtered }
        }));
    }
    
    /**
     * Create photo gallery HTML
     */
    createGalleryHTML(photos, editable = false) {
        if (!photos || photos.length === 0) {
            return '<div class="no-photos" style="text-align: center; padding: 40px; color: #64748b;">📷 No photos yet</div>';
        }
        
        const photosHTML = photos.map((photo, index) => `
            <div class="photo-item" data-photo-id="${photo.id}" style="position: relative; border-radius: 12px; overflow: hidden; aspect-ratio: 4/3;">
                <img src="${photo.data || photo.firebaseUrl}" alt="Recipe photo ${index + 1}" 
                     style="width: 100%; height: 100%; object-fit: cover; cursor: pointer;"
                     onclick="window.recipePhotoManager.viewPhotoFullscreen('${photo.id}', '${photo.data || photo.firebaseUrl}')">
                ${editable ? `
                    <button onclick="window.recipePhotoManager.deletePhoto('${photo.recipeId}', '${photo.id}')"
                            style="position: absolute; top: 8px; right: 8px; background: rgba(239, 68, 68, 0.9); color: white; border: none; border-radius: 50%; width: 32px; height: 32px; cursor: pointer; font-size: 18px; display: flex; align-items: center; justify-content: center;">
                        ×
                    </button>
                ` : ''}
                ${index === 0 ? '<div style="position: absolute; bottom: 8px; left: 8px; background: rgba(102, 126, 234, 0.9); color: white; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 700;">Main Photo</div>' : ''}
            </div>
        `).join('');
        
        return `
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px;">
                ${photosHTML}
            </div>
        `;
    }
    
    /**
     * View photo fullscreen
     */
    viewPhotoFullscreen(photoId, photoUrl) {
        const modal = document.createElement('div');
        modal.className = 'photo-fullscreen-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        `;
        
        modal.innerHTML = `
            <button onclick="this.closest('.photo-fullscreen-modal').remove()" 
                    style="position: absolute; top: 20px; right: 20px; background: rgba(255, 255, 255, 0.9); border: none; border-radius: 50%; width: 48px; height: 48px; cursor: pointer; font-size: 28px; z-index: 10001;">
                ×
            </button>
            <img src="${photoUrl}" alt="Recipe photo" 
                 style="max-width: 90%; max-height: 90%; object-fit: contain; border-radius: 8px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);">
        `;
        
        // Close on click outside image
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        // Close on Escape key
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
        
        document.body.appendChild(modal);
    }
    
    /**
     * Create upload button
     */
    createUploadButton(recipeId, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const uploadHTML = `
            <div class="photo-upload-section" style="margin-bottom: 24px;">
                <input type="file" id="photo-upload-input-${recipeId}" accept="image/jpeg,image/jpg,image/png,image/webp" multiple style="display: none;">
                <button onclick="document.getElementById('photo-upload-input-${recipeId}').click()" 
                        class="btn btn-secondary" 
                        style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;">
                    📸 Upload Photos (up to ${this.maxPhotos})
                </button>
                <div style="font-size: 12px; color: #64748b; margin-top: 8px; text-align: center;">
                    JPEG, PNG, WebP • Max 5MB per photo
                </div>
            </div>
        `;
        
        container.innerHTML = uploadHTML + container.innerHTML;
        
        // Add event listener
        const input = document.getElementById(`photo-upload-input-${recipeId}`);
        input.addEventListener('change', async (e) => {
            const files = Array.from(e.target.files);
            if (files.length > 0) {
                const loaderId = showLoading(`Uploading ${files.length} photo(s)...`);
                await this.uploadPhotos(recipeId, files);
                hideLoading(loaderId);
                
                // Refresh gallery
                this.refreshGallery(recipeId, containerId);
            }
            e.target.value = ''; // Reset input
        });
    }
    
    /**
     * Refresh gallery display
     */
    refreshGallery(recipeId, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const photos = this.getRecipePhotos(recipeId);
        const galleryDiv = container.querySelector('.photo-gallery');
        
        if (galleryDiv) {
            galleryDiv.innerHTML = this.createGalleryHTML(photos, true);
        }
    }
    
    /**
     * Get primary photo for a recipe (for thumbnails)
     */
    getPrimaryPhoto(recipeId) {
        const photos = this.getRecipePhotos(recipeId);
        return photos.length > 0 ? photos[0] : null;
    }
}

// Initialize global photo manager
window.recipePhotoManager = new RecipePhotoManager();

console.log('✅ Recipe Photo Manager available globally');

