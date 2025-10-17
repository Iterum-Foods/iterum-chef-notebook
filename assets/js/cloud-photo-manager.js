/**
 * Cloud Photo Manager - Firebase Storage Integration
 * Stores photos in Firebase Cloud Storage instead of localStorage
 */

class CloudPhotoManager {
  constructor() {
    this.storage = null;
    this.isInitialized = false;
    this.maxFileSizePhotos = 10 * 1024 * 1024; // 10 MB limit
    this.compressionQuality = 0.8; // 80% quality
    this.maxPhotoWidth = 1920;
    this.maxPhotoHeight = 1920;
    this.init();
  }

  async init() {
    try {
      console.log('☁️ Initializing Cloud Photo Manager...');

      // Wait for Firebase to be ready
      if (!window.firebase || !window.firebase.storage) {
        console.log('⏳ Waiting for Firebase Storage...');
        await this.waitForFirebase();
      }

      // Initialize Firebase Storage
      this.storage = window.firebase.storage();
      this.isInitialized = true;

      console.log('✅ Cloud Photo Manager initialized');
      console.log('📦 Storage Bucket:', window.firebaseConfig?.storageBucket);

    } catch (error) {
      console.error('❌ Failed to initialize Cloud Photo Manager:', error);
      this.isInitialized = false;
    }
  }

  /**
   * Wait for Firebase to load
   */
  async waitForFirebase() {
    return new Promise((resolve, reject) => {
      let attempts = 0;
      const maxAttempts = 50;

      const checkFirebase = setInterval(() => {
        attempts++;
        
        if (window.firebase && window.firebase.storage) {
          clearInterval(checkFirebase);
          resolve();
        } else if (attempts >= maxAttempts) {
          clearInterval(checkFirebase);
          reject(new Error('Firebase did not load in time'));
        }
      }, 100);
    });
  }

  /**
   * Upload photo to Firebase Storage
   * @param {File} file - Image file
   * @param {string} category - 'recipe', 'step', 'ingredient', 'equipment'
   * @param {string} entityId - ID of the entity (recipe ID, ingredient ID, etc.)
   * @param {number} index - Optional index for multiple photos
   */
  async uploadPhoto(file, category, entityId, index = 0) {
    try {
      if (!this.isInitialized) {
        throw new Error('Cloud Photo Manager not initialized');
      }

      if (!window.authManager?.isAuthenticated()) {
        throw new Error('User must be authenticated to upload photos');
      }

      console.log(`☁️ Uploading photo to cloud: ${file.name}`);

      // Compress image if needed
      const compressedFile = await this.compressImage(file);

      // Generate storage path
      const userId = window.authManager.currentUser.userId;
      const timestamp = Date.now();
      const fileName = `${timestamp}_${file.name.replace(/[^a-zA-Z0-9._-]/g, '_')}`;
      const storagePath = `users/${userId}/${category}/${entityId}/${fileName}`;

      // Upload to Firebase Storage
      const storageRef = this.storage.ref(storagePath);
      const uploadTask = await storageRef.put(compressedFile);

      // Get download URL
      const downloadURL = await uploadTask.ref.getDownloadURL();

      // Create photo metadata
      const photoData = {
        id: `cloud_${timestamp}_${index}`,
        url: downloadURL,
        storagePath: storagePath,
        fileName: fileName,
        category: category,
        entityId: entityId,
        index: index,
        size: compressedFile.size,
        originalSize: file.size,
        uploadedAt: new Date().toISOString(),
        uploadedBy: userId
      };

      // Save metadata to localStorage for quick access
      this.savePhotoMetadata(photoData);

      console.log(`✅ Photo uploaded to cloud: ${downloadURL}`);
      
      // Track analytics
      if (window.analyticsTracker) {
        window.analyticsTracker.trackCustomEvent('photo_uploaded', {
          category: category,
          size_kb: Math.round(compressedFile.size / 1024),
          storage: 'cloud'
        });
      }

      return photoData;

    } catch (error) {
      console.error('❌ Error uploading photo to cloud:', error);
      
      // Fallback to localStorage if cloud upload fails
      console.log('⚠️ Falling back to localStorage...');
      return await this.uploadToLocalStorage(file, category, entityId, index);
    }
  }

  /**
   * Compress image before upload
   */
  async compressImage(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        const img = new Image();
        
        img.onload = () => {
          // Calculate new dimensions
          let width = img.width;
          let height = img.height;
          
          if (width > this.maxPhotoWidth || height > this.maxPhotoHeight) {
            const ratio = Math.min(this.maxPhotoWidth / width, this.maxPhotoHeight / height);
            width = Math.round(width * ratio);
            height = Math.round(height * ratio);
          }

          // Create canvas and compress
          const canvas = document.createElement('canvas');
          canvas.width = width;
          canvas.height = height;
          
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);

          // Convert to blob
          canvas.toBlob(
            (blob) => {
              if (blob) {
                resolve(new File([blob], file.name, { type: 'image/jpeg' }));
              } else {
                reject(new Error('Compression failed'));
              }
            },
            'image/jpeg',
            this.compressionQuality
          );
        };

        img.onerror = reject;
        img.src = e.target.result;
      };

      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  /**
   * Fallback: Upload to localStorage
   */
  async uploadToLocalStorage(file, category, entityId, index) {
    const reader = new FileReader();
    
    return new Promise((resolve, reject) => {
      reader.onload = (e) => {
        const base64 = e.target.result;
        const photoData = {
          id: `local_${Date.now()}_${index}`,
          url: base64,
          storagePath: 'localStorage',
          fileName: file.name,
          category: category,
          entityId: entityId,
          index: index,
          size: base64.length,
          originalSize: file.size,
          uploadedAt: new Date().toISOString(),
          uploadedBy: 'local'
        };

        this.savePhotoMetadata(photoData);
        resolve(photoData);
      };

      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  /**
   * Save photo metadata to localStorage
   */
  savePhotoMetadata(photoData) {
    const photos = JSON.parse(localStorage.getItem('recipe_photos') || '[]');
    photos.push(photoData);
    localStorage.setItem('recipe_photos', JSON.stringify(photos));
  }

  /**
   * Get photos for an entity
   */
  getPhotos(category, entityId) {
    const photos = JSON.parse(localStorage.getItem('recipe_photos') || '[]');
    return photos.filter(p => p.category === category && p.entityId === entityId);
  }

  /**
   * Delete photo from cloud storage
   */
  async deletePhoto(photoId) {
    try {
      // Get photo metadata
      const photos = JSON.parse(localStorage.getItem('recipe_photos') || '[]');
      const photo = photos.find(p => p.id === photoId);

      if (!photo) {
        throw new Error('Photo not found');
      }

      // Delete from cloud if it's a cloud photo
      if (photo.storagePath !== 'localStorage' && this.isInitialized) {
        const storageRef = this.storage.ref(photo.storagePath);
        await storageRef.delete();
        console.log(`✅ Photo deleted from cloud: ${photo.storagePath}`);
      }

      // Remove metadata from localStorage
      const updatedPhotos = photos.filter(p => p.id !== photoId);
      localStorage.setItem('recipe_photos', JSON.stringify(updatedPhotos));

      console.log(`✅ Photo metadata removed: ${photoId}`);

      // Track analytics
      if (window.analyticsTracker) {
        window.analyticsTracker.trackCustomEvent('photo_deleted', {
          category: photo.category,
          storage: photo.storagePath === 'localStorage' ? 'local' : 'cloud'
        });
      }

      return true;

    } catch (error) {
      console.error('❌ Error deleting photo:', error);
      return false;
    }
  }

  /**
   * Migrate existing localStorage photos to cloud
   */
  async migrateLocalPhotosToCloud() {
    if (!this.isInitialized) {
      console.error('Cloud Photo Manager not initialized');
      return { success: 0, failed: 0 };
    }

    if (!window.authManager?.isAuthenticated()) {
      console.error('User must be authenticated to migrate photos');
      return { success: 0, failed: 0 };
    }

    console.log('🔄 Starting photo migration to cloud...');

    const photos = JSON.parse(localStorage.getItem('recipe_photos') || '[]');
    const localPhotos = photos.filter(p => p.storagePath === 'localStorage');

    let success = 0;
    let failed = 0;

    for (const photo of localPhotos) {
      try {
        // Convert base64 to blob
        const response = await fetch(photo.url);
        const blob = await response.blob();
        const file = new File([blob], photo.fileName, { type: 'image/jpeg' });

        // Upload to cloud
        const newPhoto = await this.uploadPhoto(file, photo.category, photo.entityId, photo.index);

        // Remove old photo
        if (newPhoto) {
          const updatedPhotos = photos.filter(p => p.id !== photo.id);
          localStorage.setItem('recipe_photos', JSON.stringify(updatedPhotos));
          success++;
        }

      } catch (error) {
        console.error(`Failed to migrate photo ${photo.id}:`, error);
        failed++;
      }
    }

    console.log(`✅ Photo migration complete: ${success} success, ${failed} failed`);
    return { success, failed };
  }

  /**
   * Get storage statistics
   */
  getStorageStats() {
    const photos = JSON.parse(localStorage.getItem('recipe_photos') || '[]');
    const cloudPhotos = photos.filter(p => p.storagePath !== 'localStorage');
    const localPhotos = photos.filter(p => p.storagePath === 'localStorage');

    const cloudSize = cloudPhotos.reduce((sum, p) => sum + (p.size || 0), 0);
    const localSize = localPhotos.reduce((sum, p) => sum + (p.size || 0), 0);

    return {
      total: photos.length,
      cloud: cloudPhotos.length,
      local: localPhotos.length,
      cloudSizeMB: (cloudSize / 1024 / 1024).toFixed(2),
      localSizeMB: (localSize / 1024 / 1024).toFixed(2),
      totalSizeMB: ((cloudSize + localSize) / 1024 / 1024).toFixed(2)
    };
  }
}

// Initialize global instance
window.cloudPhotoManager = new CloudPhotoManager();

console.log('☁️ Cloud Photo Manager loaded');

