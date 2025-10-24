# 🏗️ USTA - Technical Architecture Document

## Document Overview

**Project:** Usta - Professional Skills Platform  
**Version:** 1.0  
**Date:** October 2025  
**Author:** Iterum Foods Tech Team  

---

## 1. System Overview

### Vision
Usta is a mobile-first platform combining TikTok's ease, Instagram's social features, LinkedIn's professional value, Masterclass's expert learning, and Duolingo's gamification into one seamless experience for building professional skills.

### Core Principles
- **Mobile-First:** Primary experience is vertical video on mobile
- **Performance:** Fast, smooth scrolling like TikTok
- **Scalability:** Support millions of users and videos
- **Real-Time:** Instant validation, live feeds, immediate feedback
- **Reliability:** 99.9% uptime for professional platform
- **Security:** Protect user data and content

---

## 2. Technology Stack

### Frontend - Mobile Apps

#### **Primary: React Native**
**Why:** Write once, deploy to iOS & Android

```javascript
Framework: React Native 0.72+
Language: TypeScript
State Management: Redux Toolkit + RTK Query
Navigation: React Navigation 6
UI Components: React Native Paper + Custom
Video Player: react-native-video + Custom Controls
Camera: react-native-camera or Expo Camera
```

**Key Libraries:**
- `@react-native-async-storage/async-storage` - Local persistence
- `react-native-reanimated` - Smooth animations
- `react-native-gesture-handler` - Swipe gestures
- `react-native-firebase` - Push notifications, analytics
- `react-query` - Data fetching & caching
- `zustand` or `redux` - Global state

**Alternative: Flutter**
- If team has Dart expertise
- Slightly better performance
- Growing ecosystem

### Frontend - Web App

#### **Next.js 14+ (App Router)**
**Why:** SEO, server-side rendering for marketing pages

```javascript
Framework: Next.js 14 (App Router)
Language: TypeScript
Styling: Tailwind CSS + Usta Brand CSS
State: React Context + TanStack Query
Auth: NextAuth.js
Deployment: Vercel or AWS Amplify
```

**Structure:**
```
app/
├── (marketing)/           # Public pages
│   ├── page.tsx          # Landing page
│   ├── about/
│   ├── pricing/
│   └── pitch/            # Investor deck
├── (app)/                # Authenticated app
│   ├── feed/             # Main feed
│   ├── challenges/
│   ├── profile/
│   └── jobs/
└── api/                  # API routes
```

---

### Backend - API Server

#### **Option A: Node.js + Express (Recommended)**
**Why:** JavaScript everywhere, huge ecosystem

```javascript
Runtime: Node.js 20 LTS
Framework: Express.js or Fastify
Language: TypeScript
ORM: Prisma or TypeORM
Validation: Zod
Auth: JWT + Passport.js
Documentation: Swagger/OpenAPI
```

**Structure:**
```
src/
├── modules/
│   ├── users/
│   ├── videos/
│   ├── challenges/
│   ├── validations/
│   ├── jobs/
│   └── analytics/
├── shared/
│   ├── middleware/
│   ├── utils/
│   └── types/
└── app.ts
```

#### **Option B: Python + FastAPI**
**Why:** Great for ML/AI features (skill matching, recommendations)

```python
Framework: FastAPI
Language: Python 3.11+
ORM: SQLAlchemy or Prisma (if available)
Validation: Pydantic
Auth: JWT + OAuth2
```

**Use Python if:**
- Planning heavy ML features
- Video processing/analysis
- Team has Python expertise

---

### Database

#### **Primary Database: PostgreSQL 15+**
**Why:** Relational data, ACID compliance, JSON support

```sql
Hosting: AWS RDS or Supabase
Version: PostgreSQL 15+
Replication: Multi-AZ for reliability
Backup: Daily automated backups
Connection Pooling: PgBouncer
```

**Schema Overview:**
```sql
-- Core Tables
users
videos
challenges
skills
validations
xp_transactions
user_progress
jobs
applications

-- Relationship Tables
user_followers
challenge_completions
skill_endorsements
video_likes
video_comments
```

#### **Cache Layer: Redis**
**Why:** Fast reads, session storage, real-time features

```
Use Cases:
- Session storage
- Rate limiting
- Real-time feeds
- Trending calculations
- Job queue (Bull/BullMQ)
```

#### **Search: Elasticsearch or Algolia**
**Why:** Fast, relevant search

```
Index:
- Users (by name, skills, bio)
- Challenges (by title, tags, category)
- Jobs (by title, company, skills)
- Videos (by caption, tags)
```

---

### File Storage & Video

#### **Video Storage: AWS S3 + CloudFront CDN**

```
Workflow:
1. User records video on mobile
2. Upload to S3 (presigned URL)
3. Lambda triggers processing
4. Store multiple qualities
5. Serve via CloudFront CDN
```

**Video Processing:**
```javascript
Tool: AWS MediaConvert or FFmpeg Lambda

Process:
- Original upload → S3
- Generate thumbnails (3 frames)
- Transcode to multiple qualities:
  - 1080p (original)
  - 720p (HD)
  - 480p (mobile)
  - 360p (slow connections)
- HLS streaming for adaptive bitrate
```

**Alternative: Mux.com**
- Video hosting specialized
- Automatic transcoding
- Analytics included
- $0.005 per minute viewed
- Easier but more expensive

---

### Real-Time Features

#### **WebSockets: Socket.io or Pusher**

```javascript
Use Cases:
- Live notifications
- Real-time comments
- Live validation updates
- Challenge participation counts
- Trending updates
```

**Implementation:**
```javascript
// Server
io.on('connection', (socket) => {
  socket.on('join_challenge', (challengeId) => {
    socket.join(`challenge:${challengeId}`);
  });
  
  socket.on('validate_skill', (data) => {
    io.to(`challenge:${data.challengeId}`)
      .emit('new_validation', data);
  });
});
```

---

### Authentication & Authorization

#### **Auth Strategy: JWT + Refresh Tokens**

```javascript
Access Token:
- Short-lived (15 minutes)
- Contains user ID, role
- Stored in memory (mobile) or httpOnly cookie (web)

Refresh Token:
- Long-lived (30 days)
- Stored securely
- Used to get new access token
- Revokable via database

OAuth Providers:
- Google
- Apple
- LinkedIn (for professional verification)
```

**Session Storage:**
```javascript
// Redis structure
sessions:{userId} → {
  refreshToken: "...",
  deviceId: "...",
  lastActive: timestamp,
  ipAddress: "..."
}
```

---

### Push Notifications

#### **Firebase Cloud Messaging (FCM)**

```javascript
Triggers:
- New challenge from followed Usta
- Skill validated by peer
- Job match found
- Daily streak reminder
- Weekly progress summary
```

**Implementation:**
```javascript
// Send notification
await admin.messaging().send({
  token: userDevice.fcmToken,
  notification: {
    title: 'Skill Validated! ✅',
    body: '47 ustas validated your welding skill'
  },
  data: {
    type: 'validation',
    videoId: '12345',
    route: '/profile/skills'
  }
});
```

---

### Analytics & Tracking

#### **Product Analytics: Mixpanel or Amplitude**

```javascript
Key Events:
- User signed up
- Challenge viewed
- Challenge started
- Video recorded
- Video posted
- Skill validated
- Profile viewed
- Job applied
- Daily login
- Streak maintained
```

**Implementation:**
```javascript
// Track event
mixpanel.track('Challenge Started', {
  challengeId: challenge.id,
  challengeType: challenge.category,
  ustaCreator: challenge.creatorId,
  userLevel: user.level,
  timestamp: new Date()
});
```

#### **Error Tracking: Sentry**

```javascript
Monitors:
- Crashes
- API errors
- Performance issues
- User feedback
```

---

### CI/CD Pipeline

#### **GitHub Actions**

```yaml
# .github/workflows/deploy.yml

Mobile:
- Run tests
- Build iOS (TestFlight)
- Build Android (Play Store)
- Deploy to staging
- Manual approve → Production

Backend:
- Run tests
- Build Docker image
- Push to ECR
- Deploy to ECS/Lambda
- Run smoke tests

Web:
- Run tests
- Build Next.js
- Deploy to Vercel
- Run Lighthouse
```

---

## 3. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    MOBILE APPS                          │
│              iOS (React Native)                         │
│              Android (React Native)                     │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             ├────────────────────────────┤
             │                            │
┌────────────▼────────────┐   ┌──────────▼──────────────┐
│     API GATEWAY         │   │   WEB APP (Next.js)     │
│   (AWS API Gateway)     │   │   Hosted on Vercel      │
└────────────┬────────────┘   └──────────┬──────────────┘
             │                           │
             └───────────┬───────────────┘
                         │
             ┌───────────▼────────────┐
             │   LOAD BALANCER        │
             │   (AWS ALB)            │
             └───────────┬────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐
│   API        │  │   API       │  │   API      │
│   Server 1   │  │   Server 2  │  │   Server N │
│   (Node.js)  │  │   (Node.js) │  │  (Node.js) │
└───────┬──────┘  └──────┬──────┘  └─────┬──────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌─────▼──────────┐
│ PostgreSQL   │  │   Redis     │  │  Elasticsearch │
│   (RDS)      │  │   Cache     │  │    Search      │
└──────────────┘  └─────────────┘  └────────────────┘

        ┌─────────────────────────────────┐
        │     VIDEO PROCESSING            │
        ├─────────────────────────────────┤
        │  S3 Storage                     │
        │  Lambda Processor               │
        │  MediaConvert                   │
        │  CloudFront CDN                 │
        └─────────────────────────────────┘

        ┌─────────────────────────────────┐
        │     EXTERNAL SERVICES           │
        ├─────────────────────────────────┤
        │  Firebase (Push, Analytics)     │
        │  Mixpanel (Product Analytics)   │
        │  Sentry (Error Tracking)        │
        │  Stripe (Payments)              │
        └─────────────────────────────────┘
```

---

## 4. Data Models

### Core Entities

#### **User**
```typescript
interface User {
  id: string;
  email: string;
  username: string;
  displayName: string;
  bio?: string;
  avatarUrl?: string;
  
  // Progression
  level: 'novice' | 'apprentice' | 'journeyman' | 'usta' | 'master_usta';
  totalXP: number;
  currentStreak: number;
  longestStreak: number;
  
  // Stats
  videosPosted: number;
  challengesCompleted: number;
  skillsValidated: number;
  followersCount: number;
  followingCount: number;
  
  // Profile
  industries: string[];
  skills: Skill[];
  location?: string;
  website?: string;
  linkedinUrl?: string;
  
  // Settings
  isUsta: boolean;
  isMasterUsta: boolean;
  canCreateChallenges: boolean;
  premiumUntil?: Date;
  
  createdAt: Date;
  updatedAt: Date;
}
```

#### **Challenge**
```typescript
interface Challenge {
  id: string;
  creatorId: string; // Usta who created it
  
  title: string;
  description: string;
  category: string; // 'welding', 'coding', 'cooking', etc.
  difficulty: 1 | 2 | 3 | 4 | 5;
  estimatedTime: number; // minutes
  
  // Media
  demoVideoUrl: string;
  thumbnailUrl: string;
  
  // Recording Template
  recordingGuide: {
    shots: Array<{
      name: string;
      duration: number;
      instruction: string;
    }>;
    tips: string[];
  };
  
  // Gamification
  xpReward: number;
  badgeId?: string;
  
  // Stats
  participantCount: number;
  completionCount: number;
  averageRating: number;
  
  // Visibility
  isActive: boolean;
  isFeatured: boolean;
  isTrending: boolean;
  
  createdAt: Date;
  expiresAt?: Date;
}
```

#### **Video (User Submission)**
```typescript
interface Video {
  id: string;
  userId: string;
  challengeId?: string;
  
  // Media
  videoUrl: string;
  thumbnailUrl: string;
  duration: number;
  
  // Content
  caption?: string;
  hashtags: string[];
  
  // Processing
  status: 'processing' | 'ready' | 'failed';
  qualities: {
    '1080p': string;
    '720p': string;
    '480p': string;
    '360p': string;
  };
  
  // Engagement
  viewCount: number;
  likeCount: number;
  commentCount: number;
  shareCount: number;
  
  // Validation
  validationCount: number;
  validatedBy: string[]; // User IDs
  isValidated: boolean;
  
  // Visibility
  isPublic: boolean;
  isDeleted: boolean;
  
  createdAt: Date;
}
```

#### **Skill**
```typescript
interface Skill {
  id: string;
  name: string;
  category: string;
  level: 1 | 2 | 3 | 4 | 5;
  
  // Validation
  validationCount: number;
  validatedBy: Array<{
    userId: string;
    validatedAt: Date;
    rating: number;
  }>;
  
  // Evidence
  videoIds: string[];
  certificateIds?: string[];
  
  createdAt: Date;
  lastValidatedAt: Date;
}
```

#### **Job Posting**
```typescript
interface JobPosting {
  id: string;
  companyId: string;
  
  title: string;
  description: string;
  requirements: string[];
  
  // Matching
  requiredSkills: string[];
  experienceLevel: string;
  location: string;
  isRemote: boolean;
  
  // Compensation
  salaryMin?: number;
  salaryMax?: number;
  currency: string;
  
  // Posting
  tier: 'basic' | 'premium' | 'featured';
  expiresAt: Date;
  
  // Stats
  viewCount: number;
  applicationCount: number;
  
  isActive: boolean;
  createdAt: Date;
}
```

---

## 5. API Design

### RESTful Endpoints

#### **Authentication**
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
```

#### **Users**
```
GET    /api/v1/users/me
PATCH  /api/v1/users/me
GET    /api/v1/users/:id
GET    /api/v1/users/:id/videos
GET    /api/v1/users/:id/skills
POST   /api/v1/users/:id/follow
DELETE /api/v1/users/:id/follow
```

#### **Challenges**
```
GET    /api/v1/challenges              # List all
GET    /api/v1/challenges/trending     # Trending
GET    /api/v1/challenges/:id          # Details
POST   /api/v1/challenges/:id/start    # Start challenge
POST   /api/v1/challenges               # Create (Usta only)
PATCH  /api/v1/challenges/:id          # Update
```

#### **Videos**
```
GET    /api/v1/videos/feed             # Main feed
GET    /api/v1/videos/:id              # Single video
POST   /api/v1/videos                  # Upload
DELETE /api/v1/videos/:id              # Delete
POST   /api/v1/videos/:id/like         # Like
POST   /api/v1/videos/:id/validate     # Validate skill
POST   /api/v1/videos/:id/comment      # Comment
GET    /api/v1/videos/:id/comments     # Get comments
```

#### **Skills**
```
GET    /api/v1/skills                  # Browse skills
GET    /api/v1/skills/:id              # Skill details
POST   /api/v1/skills/:id/validate     # Validate someone's skill
```

#### **Jobs**
```
GET    /api/v1/jobs                    # List jobs
GET    /api/v1/jobs/:id                # Job details
POST   /api/v1/jobs/:id/apply          # Apply
POST   /api/v1/jobs                    # Post job (employers)
```

#### **XP & Progress**
```
GET    /api/v1/me/progress             # User progress
GET    /api/v1/me/xp-history           # XP transactions
GET    /api/v1/me/streak               # Streak info
```

---

## 6. Video Infrastructure

### Upload Flow

```
1. User records video in app
   ↓
2. Request presigned S3 URL from backend
   POST /api/v1/videos/upload-url
   Response: { uploadUrl, videoId }
   ↓
3. Upload directly to S3 (bypass backend)
   PUT {uploadUrl}
   ↓
4. S3 triggers Lambda on upload complete
   ↓
5. Lambda processes video:
   - Extract 3 thumbnail frames
   - Transcode to 4 qualities
   - Calculate duration
   - Generate HLS manifest
   ↓
6. Update database: status = 'ready'
   ↓
7. Notify user via WebSocket
   ↓
8. Video appears in feed
```

### Video Serving

```
Request: GET /api/v1/videos/abc123/stream

Response:
{
  "hlsUrl": "https://cdn.usta.com/videos/abc123/master.m3u8",
  "thumbnails": [
    "https://cdn.usta.com/videos/abc123/thumb_0.jpg",
    "https://cdn.usta.com/videos/abc123/thumb_1.jpg",
    "https://cdn.usta.com/videos/abc123/thumb_2.jpg"
  ],
  "duration": 45,
  "qualities": ["1080p", "720p", "480p", "360p"]
}
```

---

## 7. Scaling Strategy

### Phase 1: 0-10K Users (Months 1-6)
**Infrastructure:**
- Single API server (t3.medium)
- Single RDS instance (db.t3.small)
- Single Redis instance
- S3 + CloudFront

**Cost:** ~$500/month

### Phase 2: 10K-100K Users (Months 7-12)
**Infrastructure:**
- 3-5 API servers (auto-scaling)
- RDS read replicas (2x)
- Redis cluster (3 nodes)
- CloudFront with more edge locations

**Cost:** ~$2,000/month

### Phase 3: 100K-1M Users (Year 2)
**Infrastructure:**
- Auto-scaling API servers (10-50)
- Multi-AZ RDS with read replicas
- Redis cluster (6 nodes)
- Elasticsearch cluster
- Separate video processing cluster

**Cost:** ~$10,000/month

### Phase 4: 1M+ Users (Year 3+)
**Infrastructure:**
- Kubernetes for container orchestration
- Multi-region deployment
- Database sharding
- Microservices architecture
- Dedicated team for infrastructure

**Cost:** ~$50,000/month

---

## 8. Security Considerations

### Data Protection
```
- All data encrypted at rest (AES-256)
- All traffic encrypted in transit (TLS 1.3)
- Sensitive data (passwords) hashed with bcrypt
- PII data anonymized in analytics
- GDPR & CCPA compliant
```

### API Security
```
- Rate limiting (100 req/min per user)
- CORS configured properly
- SQL injection prevention (parameterized queries)
- XSS prevention (sanitize inputs)
- CSRF tokens for web
- JWT signature verification
```

### Video Security
```
- Presigned URLs (expire in 1 hour)
- Content moderation (AWS Rekognition)
- Watermarking for premium content
- DMCA takedown process
```

---

## 9. Monitoring & Observability

### Application Monitoring
```
Tool: Datadog or New Relic

Metrics:
- API response times
- Error rates
- Database query performance
- Cache hit rates
- Video processing times
```

### Alerts
```
- API error rate > 1%
- Response time > 500ms (p95)
- Database connections > 80%
- Disk space > 85%
- Failed video processing > 5%
```

### Logging
```
Tool: AWS CloudWatch or Datadog

Levels:
- ERROR: Critical issues
- WARN: Potential issues
- INFO: Key events
- DEBUG: Development only
```

---

## 10. Deployment Architecture

### Production Environment

```
Region: us-east-1 (primary)
Backup Region: us-west-2

Environments:
- Production (prod)
- Staging (staging)
- Development (dev)

Deploy Process:
1. Developer pushes to main
2. Tests run automatically
3. Build Docker image
4. Deploy to staging
5. Run smoke tests
6. Manual approval
7. Blue-green deploy to production
8. Monitor for 15 minutes
9. Rollback if issues
```

---

## 11. Technology Decisions Summary

| Component | Choice | Why |
|-----------|--------|-----|
| **Mobile** | React Native | Cross-platform, large community |
| **Web** | Next.js | SEO, performance, React ecosystem |
| **Backend** | Node.js + Express | JavaScript everywhere, fast development |
| **Database** | PostgreSQL | Relational data, JSON support, mature |
| **Cache** | Redis | Fast, proven, real-time features |
| **File Storage** | AWS S3 | Scalable, cheap, reliable |
| **CDN** | CloudFront | AWS integration, global reach |
| **Video Processing** | AWS MediaConvert | Managed, scalable |
| **Auth** | JWT + Firebase | Flexible, secure |
| **Push** | Firebase FCM | Free, reliable, cross-platform |
| **Analytics** | Mixpanel | Product analytics focused |
| **Errors** | Sentry | Best error tracking |
| **Hosting** | AWS | Complete ecosystem, scalable |

---

## 12. Development Timeline

### Month 1-2: Foundation
- [ ] Set up repositories
- [ ] Configure CI/CD
- [ ] Set up AWS infrastructure
- [ ] Create API boilerplate
- [ ] Set up database
- [ ] Mobile app boilerplate

### Month 3-4: Core Features
- [ ] User authentication
- [ ] Video upload & playback
- [ ] Challenge system
- [ ] Basic feed
- [ ] Profile pages

### Month 5-6: MVP Complete
- [ ] Validation system
- [ ] XP & levels
- [ ] Push notifications
- [ ] Search
- [ ] Testing & polish

### Month 7-8: Beta
- [ ] Job board
- [ ] Premium features
- [ ] Analytics dashboard
- [ ] Content moderation
- [ ] Performance optimization

### Month 9+: Scale
- [ ] Microservices migration
- [ ] Advanced features
- [ ] International expansion
- [ ] ML recommendations

---

## 13. Cost Estimates

### Year 1 (0-50K users)
```
AWS Infrastructure:      $6,000/year
Video Storage/CDN:       $12,000/year
Firebase:                $2,400/year
Mixpanel:                $3,000/year
Sentry:                  $1,200/year
Development Tools:       $2,400/year
TOTAL:                   ~$27,000/year ($2,250/month)
```

### Year 2 (50K-250K users)
```
AWS Infrastructure:      $24,000/year
Video Storage/CDN:       $60,000/year
Third-party services:    $12,000/year
TOTAL:                   ~$96,000/year ($8,000/month)
```

### Year 3 (250K-750K users)
```
AWS Infrastructure:      $120,000/year
Video Storage/CDN:       $240,000/year
Third-party services:    $30,000/year
TOTAL:                   ~$390,000/year ($32,500/month)
```

---

## 14. Risks & Mitigation

### Technical Risks

**1. Video Processing Costs**
- Risk: High volume = expensive transcoding
- Mitigation: Batch processing, user-pays for premium quality

**2. Database Performance**
- Risk: Slow queries at scale
- Mitigation: Proper indexing, caching, read replicas

**3. Real-time Feed Performance**
- Risk: Slow feed = poor UX
- Mitigation: Aggressive caching, CDN, pagination

**4. Mobile App Size**
- Risk: Large app = fewer downloads
- Mitigation: Code splitting, on-demand downloads

---

## 15. Success Metrics

### Technical KPIs
```
- API response time: < 200ms (p95)
- Video processing time: < 2 minutes
- App crash rate: < 0.1%
- Uptime: > 99.9%
- CDN cache hit rate: > 90%
```

### Performance Targets
```
- Feed load time: < 1 second
- Video start time: < 500ms
- Search results: < 300ms
- Profile load: < 800ms
```

---

## Appendix A: Sample API Response

### GET /api/v1/videos/feed

```json
{
  "videos": [
    {
      "id": "vid_abc123",
      "user": {
        "id": "usr_xyz789",
        "username": "weldingmaster",
        "displayName": "Mike Rodriguez",
        "avatarUrl": "https://cdn.usta.com/avatars/xyz789.jpg",
        "level": "usta",
        "isVerified": true
      },
      "challenge": {
        "id": "chal_123",
        "title": "#WeldingBasics Challenge",
        "category": "welding"
      },
      "videoUrl": "https://cdn.usta.com/videos/abc123/master.m3u8",
      "thumbnailUrl": "https://cdn.usta.com/videos/abc123/thumb.jpg",
      "duration": 45,
      "caption": "Perfect bead on my first try! 🔥",
      "hashtags": ["#WeldingBasics", "#FirstTry", "#Usta"],
      "stats": {
        "views": 12847,
        "likes": 1043,
        "comments": 127,
        "validations": 47
      },
      "userHasLiked": false,
      "userHasValidated": false,
      "createdAt": "2025-10-20T14:30:00Z"
    }
  ],
  "cursor": "next_page_token_here",
  "hasMore": true
}
```

---

**Tech Stack Approved:** Pending  
**Infrastructure Budget:** $27K Year 1  
**Development Timeline:** 6 months to MVP  
**Scalability:** Supports 1M+ users  

🔨 **Ready to build Usta.**

