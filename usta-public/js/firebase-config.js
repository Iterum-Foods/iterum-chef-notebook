/**
 * Firebase Configuration for Usta
 * Handles Firebase Storage for video uploads
 */

// Firebase configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",  // Replace with your Firebase config
    authDomain: "iterum-culinary-app.firebaseapp.com",
    projectId: "iterum-culinary-app",
    storageBucket: "iterum-culinary-app.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase (if not already initialized)
if (typeof firebase !== 'undefined' && !firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

// Get Storage reference
const storage = firebase.storage();
const storageRef = storage.ref();

/**
 * Upload video to Firebase Storage
 * @param {File} videoFile - The video file to upload
 * @param {Function} onProgress - Callback for upload progress (0-100)
 * @returns {Promise<string>} - URL of uploaded video
 */
async function uploadVideoToFirebase(videoFile, onProgress) {
    return new Promise((resolve, reject) => {
        // Generate unique filename
        const timestamp = Date.now();
        const randomId = Math.random().toString(36).substring(7);
        const filename = `videos/${timestamp}_${randomId}_${videoFile.name}`;
        
        // Create storage reference
        const videoRef = storageRef.child(filename);
        
        // Upload file
        const uploadTask = videoRef.put(videoFile);
        
        // Monitor upload progress
        uploadTask.on('state_changed',
            (snapshot) => {
                // Progress
                const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
                if (onProgress) {
                    onProgress(Math.round(progress));
                }
            },
            (error) => {
                // Error
                console.error('Upload error:', error);
                reject(error);
            },
            async () => {
                // Complete - get download URL
                try {
                    const downloadURL = await uploadTask.snapshot.ref.getDownloadURL();
                    resolve(downloadURL);
                } catch (error) {
                    reject(error);
                }
            }
        );
    });
}

/**
 * Upload thumbnail image
 * @param {File} imageFile - The thumbnail image
 * @returns {Promise<string>} - URL of uploaded image
 */
async function uploadThumbnail(imageFile) {
    const timestamp = Date.now();
    const randomId = Math.random().toString(36).substring(7);
    const filename = `thumbnails/${timestamp}_${randomId}_${imageFile.name}`;
    
    const thumbnailRef = storageRef.child(filename);
    await thumbnailRef.put(imageFile);
    
    return await thumbnailRef.getDownloadURL();
}

/**
 * Delete video from Firebase Storage
 * @param {string} videoUrl - The video URL to delete
 */
async function deleteVideoFromFirebase(videoUrl) {
    try {
        const videoRef = storage.refFromURL(videoUrl);
        await videoRef.delete();
        return true;
    } catch (error) {
        console.error('Delete error:', error);
        return false;
    }
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        uploadVideoToFirebase,
        uploadThumbnail,
        deleteVideoFromFirebase
    };
}

