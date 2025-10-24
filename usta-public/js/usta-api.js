/**
 * Usta API Client
 * Handles all backend communication
 */

// API Base URL - automatically switches between local and production
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : 'https://usta-backend.up.railway.app/api';  // Will be updated after Railway deployment

class UstaAPI {
    constructor() {
        this.token = localStorage.getItem('usta_token');
        this.user = JSON.parse(localStorage.getItem('usta_user') || '{}');
    }

    // ==========================================
    // AUTHENTICATION
    // ==========================================

    async register(userData) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.token = data.token;
                this.user = data.user;
                localStorage.setItem('usta_token', data.token);
                localStorage.setItem('usta_user', JSON.stringify(data.user));
            }
            
            return { success: response.ok, data };
        } catch (error) {
            console.error('Register error:', error);
            return { success: false, error: error.message };
        }
    }

    async login(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.token = data.token;
                this.user = data.user;
                localStorage.setItem('usta_token', data.token);
                localStorage.setItem('usta_user', JSON.stringify(data.user));
            }
            
            return { success: response.ok, data };
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: error.message };
        }
    }

    logout() {
        this.token = null;
        this.user = {};
        localStorage.removeItem('usta_token');
        localStorage.removeItem('usta_user');
        window.location.href = 'landing.html';
    }

    isAuthenticated() {
        return !!this.token;
    }

    getCurrentUser() {
        return this.user;
    }

    // ==========================================
    // VIDEOS
    // ==========================================

    async getVideoFeed(page = 1, limit = 10) {
        try {
            const response = await fetch(
                `${API_BASE_URL}/videos/feed?page=${page}&limit=${limit}`,
                {
                    headers: this._getHeaders()
                }
            );
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Get feed error:', error);
            return { success: false, error: error.message };
        }
    }

    async uploadVideo(videoFile, metadata) {
        try {
            const formData = new FormData();
            formData.append('video', videoFile);
            formData.append('caption', metadata.caption || '');
            formData.append('challenge_id', metadata.challenge_id || '');
            
            const response = await fetch(`${API_BASE_URL}/videos/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                },
                body: formData
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Upload error:', error);
            return { success: false, error: error.message };
        }
    }

    async likeVideo(videoId) {
        try {
            const response = await fetch(`${API_BASE_URL}/videos/${videoId}/like`, {
                method: 'POST',
                headers: this._getHeaders()
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Like error:', error);
            return { success: false, error: error.message };
        }
    }

    async validateVideo(videoId) {
        try {
            const response = await fetch(`${API_BASE_URL}/videos/${videoId}/validate`, {
                method: 'POST',
                headers: this._getHeaders()
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Validate error:', error);
            return { success: false, error: error.message };
        }
    }

    // ==========================================
    // USERS
    // ==========================================

    async getUserProfile(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
                headers: this._getHeaders()
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Get profile error:', error);
            return { success: false, error: error.message };
        }
    }

    async followUser(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/users/${userId}/follow`, {
                method: 'POST',
                headers: this._getHeaders()
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Follow error:', error);
            return { success: false, error: error.message };
        }
    }

    async unfollowUser(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/users/${userId}/unfollow`, {
                method: 'DELETE',
                headers: this._getHeaders()
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Unfollow error:', error);
            return { success: false, error: error.message };
        }
    }

    async discoverUsers(craft = null) {
        try {
            const url = craft 
                ? `${API_BASE_URL}/users/discover?craft=${craft}`
                : `${API_BASE_URL}/users/discover`;
            
            const response = await fetch(url, {
                headers: this._getHeaders()
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Discover error:', error);
            return { success: false, error: error.message };
        }
    }

    // ==========================================
    // CHALLENGES
    // ==========================================

    async getChallenges(filters = {}) {
        try {
            const params = new URLSearchParams(filters);
            const response = await fetch(
                `${API_BASE_URL}/challenges?${params}`,
                {
                    headers: this._getHeaders()
                }
            );
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Get challenges error:', error);
            return { success: false, error: error.message };
        }
    }

    async getChallenge(challengeId) {
        try {
            const response = await fetch(`${API_BASE_URL}/challenges/${challengeId}`, {
                headers: this._getHeaders()
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Get challenge error:', error);
            return { success: false, error: error.message };
        }
    }

    async takeChallenge(challengeId) {
        try {
            const response = await fetch(`${API_BASE_URL}/challenges/${challengeId}/take`, {
                method: 'POST',
                headers: this._getHeaders()
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            console.error('Take challenge error:', error);
            return { success: false, error: error.message };
        }
    }

    // ==========================================
    // HELPERS
    // ==========================================

    _getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    // Demo mode fallback (when backend not available)
    _getDemoData(type) {
        const demoData = {
            videos: [
                {
                    id: 1,
                    user: {
                        id: 1,
                        username: 'masterwelder',
                        craft: 'Welding',
                        craft_icon: '🔧',
                        level: 'master_usta'
                    },
                    caption: 'Perfect TIG weld demonstration',
                    likes_count: 234,
                    validation_count: 89,
                    challenge: { title: '#WeldingBasics' }
                },
                {
                    id: 2,
                    user: {
                        id: 2,
                        username: 'chefgordon',
                        craft: 'Culinary',
                        craft_icon: '👨‍🍳',
                        level: 'master_usta'
                    },
                    caption: 'Knife skills masterclass',
                    likes_count: 456,
                    validation_count: 127,
                    challenge: { title: '#KnifeSkills' }
                }
            ]
        };
        
        return demoData[type] || [];
    }
}

// Create global API instance
const ustaAPI = new UstaAPI();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UstaAPI;
}

