# 📱 USTA - Product Requirements Document (PRD)

## Document Info
**Product:** Usta (Master Your Craft)  
**Version:** 1.0 - MVP  
**Date:** October 2025  
**Owner:** Product Team  
**Status:** Draft → Review → Approved  

---

## 1. Executive Summary

### Product Vision
Usta is the first platform that makes building a professional skills portfolio as easy as TikTok, as social as Instagram, as valuable as LinkedIn, as educational as Masterclass, and as engaging as Duolingo.

### Product Mission
Enable any skilled professional to showcase their abilities, connect with peers, learn from masters, and advance their career through guided skill challenges and peer validation.

### Success Criteria (12 months)
- 100,000 registered users
- 50,000 monthly active users (MAU)
- 500+ active challenges
- 100+ Master Ustas creating content
- 10,000+ skills validated daily
- $500K ARR

---

## 2. Target Users

### Primary Personas

#### **Persona 1: Alex the Apprentice**
- **Age:** 22-28
- **Role:** Junior developer, apprentice welder, culinary student
- **Goal:** Build portfolio to land first professional job
- **Pain:** No way to prove skills beyond resume
- **Behavior:** Active on TikTok/Instagram, learns online
- **Quote:** "I can do the work, but how do I show employers?"

**Needs:**
- Easy way to create professional content
- Validation from experienced professionals
- Portfolio that stands out
- Job matching based on skills

#### **Persona 2: Maria the Master**
- **Age:** 35-50
- **Role:** Senior developer, master electrician, executive chef
- **Goal:** Build personal brand, find better opportunities
- **Pain:** LinkedIn feels corporate, Instagram isn't professional
- **Behavior:** Mentors others, active in professional communities
- **Quote:** "I want to share my expertise and build my reputation"

**Needs:**
- Platform to showcase expertise
- Ability to mentor/validate others
- Professional networking
- Monetization for content creation

#### **Persona 3: Sam the Switcher**
- **Age:** 28-45
- **Role:** Career changer, learning new skills
- **Goal:** Prove competency in new field
- **Pain:** No formal training to show
- **Behavior:** Takes online courses, practices daily
- **Quote:** "I'm self-taught—how do I prove I know what I'm doing?"

**Needs:**
- Structured learning path
- Way to demonstrate skills
- Community support
- Credential recognition

#### **Persona 4: Rachel the Recruiter**
- **Age:** 30-45
- **Role:** HR manager, hiring manager
- **Goal:** Find qualified candidates quickly
- **Pain:** Resumes don't show actual ability
- **Behavior:** Uses LinkedIn, job boards, referrals
- **Quote:** "I need to see what they can actually do"

**Needs:**
- See real skills, not claims
- Validated abilities
- Direct access to candidates
- Efficient hiring process

---

## 3. MVP Feature Set

### Core Features (Must Have for Launch)

#### **3.1 Trending Feed (TikTok-Style)**

**Description:**
Vertical video feed showing skill demonstrations from professionals.

**User Story:**
"As a user, I want to scroll through skill demonstrations so I can discover new skills and get inspired."

**Requirements:**
- Vertical video player (9:16 aspect ratio)
- Swipe up/down navigation
- Auto-play on view
- Video controls (play, pause, mute)
- See video metadata (title, creator, challenge)
- See engagement stats (views, validations, comments)
- Infinite scroll with pagination

**Acceptance Criteria:**
- Videos load within 500ms
- Smooth 60fps scrolling
- Auto-play works 99% of time
- Can handle 1000+ videos in feed

**Priority:** P0 (Critical)

---

#### **3.2 Challenge System**

**Description:**
Master Ustas create skill challenges with guided recording templates. Users follow templates to record their version.

**User Stories:**
- "As a Master Usta, I want to create skill challenges so others can learn from me"
- "As a user, I want to follow challenge templates so I know exactly what to record"
- "As a user, I want to see trending challenges so I know what skills to demonstrate"

**Requirements:**

**Challenge Creation (Usta Only):**
- Title, description, category
- Record demonstration video (60-90 sec)
- Create recording guide:
  - 3-5 shots with timing
  - Instructions per shot
  - Tips & common mistakes
- Set difficulty level (1-5)
- Set XP reward (10-100 XP)
- Add hashtags

**Challenge Discovery:**
- Browse trending challenges
- Filter by category/difficulty
- Search challenges
- See participant count
- See completion rate

**Challenge Participation:**
- View challenge details
- Watch Usta's demo video
- See recording guide
- Tap "Try This Challenge"
- Launch camera with guide overlay
- Record following template
- Preview before posting
- Submit to challenge

**Acceptance Criteria:**
- Users can find relevant challenges < 30 seconds
- Recording guide is clear and actionable
- 80%+ completion rate when started
- Videos submitted match template quality

**Priority:** P0 (Critical)

---

#### **3.3 Guided Video Recording**

**Description:**
In-app camera with overlay guide showing what to record and when.

**User Story:**
"As a user, I want step-by-step camera guidance so I can create professional-quality skill demonstrations without video experience."

**Requirements:**

**Camera Interface:**
- Access device camera
- Vertical orientation locked
- Recording guide overlay:
  - Current shot name
  - Time remaining for shot
  - Instructions visible
  - Progress indicator
- Shot-by-shot recording:
  - "Shot 1: Show your setup (5 sec)"
  - Count down timer
  - Auto-advance to next shot
- Preview after recording
- Retake individual shots
- Trim/edit basic

**Quality Checks:**
- Minimum resolution: 720p
- Lighting warning if too dark
- Audio check (optional)
- Orientation check
- Duration requirements met

**Acceptance Criteria:**
- 90% of users complete recording on first try
- Videos meet quality standards
- Camera works on iOS & Android
- Processing < 30 seconds

**Priority:** P0 (Critical)

---

#### **3.4 User Profiles & Portfolios**

**Description:**
Professional profile showcasing validated skills, videos, and progression.

**User Story:**
"As a user, I want a professional profile that automatically organizes my validated skills so employers can see my abilities."

**Requirements:**

**Profile Components:**
- Header (avatar, name, bio, location)
- Level badge (Novice → Master Usta)
- Stats (XP, skills validated, challenges completed)
- Video grid (all submissions)
- Skills list (organized by category)
- Validation badges
- Followers/following counts
- Edit profile button (own profile)
- Follow button (other profiles)
- Message button

**Portfolio Organization:**
- Auto-organized by skill category
- Show validation count per skill
- Filter by challenge/freeform
- Sort by most validated
- Highlight featured videos

**Public vs Private:**
- Choose public/private per video
- Portfolio visibility settings
- Resume download (PDF)

**Acceptance Criteria:**
- Profile loads < 800ms
- Skills automatically categorized
- Validation badges display correctly
- Responsive on mobile & web

**Priority:** P0 (Critical)

---

#### **3.5 Skill Validation System**

**Description:**
Peer-to-peer validation where professionals validate each other's demonstrated skills.

**User Story:**
"As a professional, I want to validate others' skills so the community maintains quality and credibility."

**Requirements:**

**Validation Action:**
- Watch video
- Tap "Validate Skill" button
- Optional: Add comment/rating
- Confirmation: "Skill validated ✅"
- Notification sent to video creator

**Validation Display:**
- Show validation count on video
- Show who validated (list of profiles)
- Validation threshold for "Verified" (10+ validations)
- Usta validations worth more (2x weight)

**Anti-Gaming:**
- Can't validate own videos
- Limit: 100 validations per day
- Suspicious patterns flagged
- Validation credibility score

**Acceptance Criteria:**
- Validation is instant
- Notifications sent within 1 minute
- No gaming/spam validations
- Quality maintained

**Priority:** P0 (Critical)

---

#### **3.6 XP & Progression System**

**Description:**
Duolingo-style XP, levels, and streaks to drive daily engagement.

**User Story:**
"As a user, I want to see my progress and level up so I stay motivated to practice skills daily."

**Requirements:**

**XP Sources:**
- Complete challenge: 10-100 XP (based on difficulty)
- Validate someone's skill: 5 XP
- Daily login: 5 XP
- Maintain streak: 10 XP bonus
- Get validated: 2 XP per validation
- Complete skill path: 200 XP

**Levels:**
```
🌱 Novice      0-100 XP
🔧 Apprentice  100-500 XP
⚙️ Journeyman  500-2,000 XP
🔨 Usta        2,000-5,000 XP
⚒️ Master Usta 5,000+ XP (+ peer vote)
```

**Streaks:**
- Track consecutive days active
- Streak freeze (1 per week, Premium)
- Streak repair (Premium only)
- Leaderboard by streak

**Badges:**
- First challenge (Bronze)
- 10 challenges (Silver)
- 50 challenges (Gold)
- Specialist badges (skill-specific)
- Community badges (helping others)

**Acceptance Criteria:**
- XP awarded immediately
- Level-ups trigger celebration
- Streaks calculated correctly
- Badges display on profile

**Priority:** P0 (Critical)

---

#### **3.7 Basic Job Board**

**Description:**
Simple job posting and matching system for employers to find validated talent.

**User Story:**
"As an employer, I want to post jobs and find candidates with validated skills."

**Requirements:**

**For Employers:**
- Post job (title, description, requirements)
- Set required skills (matched to Usta skills)
- Set compensation range
- Set location/remote
- Preview before posting
- Pay $199 (Basic), $349 (Premium), $499 (Featured)

**For Job Seekers:**
- Browse jobs
- Filter by skills, location, compensation
- See match percentage
- Apply with Usta profile
- Track applications

**Matching Algorithm:**
- Match user skills to job requirements
- Calculate match percentage
- Prioritize validated skills
- Consider user level

**Acceptance Criteria:**
- Jobs post successfully
- Matching algorithm works
- Applications submitted
- Employers can view applicants

**Priority:** P1 (High - MVP+ feature)

---

#### **3.8 User Authentication**

**Description:**
Secure signup, login, and session management.

**User Story:**
"As a user, I want to securely create an account and access it across devices."

**Requirements:**

**Sign Up:**
- Email + password
- Or: Google, Apple, LinkedIn OAuth
- Email verification
- Username selection (unique)
- Profile creation flow

**Login:**
- Email/password
- OAuth options
- Remember me
- Forgot password flow

**Session Management:**
- JWT tokens (15-minute access, 30-day refresh)
- Multi-device support
- Logout (all devices option)
- Session expiry

**Acceptance Criteria:**
- 99.9% successful auth
- < 2 seconds to log in
- Secure (tokens encrypted)
- Works offline (cached session)

**Priority:** P0 (Critical)

---

#### **3.9 Follow/Social System**

**Description:**
Follow other users, see followed users' content, build network.

**User Story:**
"As a user, I want to follow professionals I admire so I can see their content and stay connected."

**Requirements:**

**Actions:**
- Follow user
- Unfollow user
- See followers list
- See following list
- Mutual follow indicator

**Feed Impact:**
- "Following" feed shows followed users' content
- "For You" feed shows algorithm-recommended content
- Toggle between feeds

**Notifications:**
- [User] followed you
- [User] you follow posted new video

**Acceptance Criteria:**
- Follow is instant
- Counts update immediately
- Following feed filters correctly
- No performance impact at scale

**Priority:** P0 (Critical)

---

### V2 Features (Post-MVP)

#### **3.10 Direct Messaging**
- 1:1 messaging
- Group chats
- Share videos in chat
- Employer → candidate messaging

**Priority:** P1 (High)

#### **3.11 Comments & Engagement**
- Comment on videos
- Like comments
- Reply threads
- @mentions

**Priority:** P1 (High)

#### **3.12 Expert Courses (Masterclass)**
- Long-form tutorials
- Course curriculum
- Video lessons
- Quizzes
- Certificates

**Priority:** P2 (Medium)

#### **3.13 Skill Trees/Paths**
- Duolingo-style progression paths
- Unlock advanced skills
- Visual skill tree
- Recommended next skills

**Priority:** P2 (Medium)

#### **3.14 Advanced Search**
- Search users, challenges, skills
- Filters
- Saved searches
- Search history

**Priority:** P2 (Medium)

---

## 4. User Flows

### Flow 1: New User Onboarding

```
1. Download app / Visit site
2. See value prop (TikTok for professional skills)
3. Sign up (email or OAuth)
4. Choose primary skill/industry
5. Set experience level
6. See 3 trending challenges in their field
7. Watch one challenge demo
8. Get prompted to try it
9. Record first video with guide
10. Post and get first validation
11. Celebrate! "First skill demonstrated 🎉"
```

**Goal:** User posts first video within 10 minutes

---

### Flow 2: Daily Active User

```
1. Open app (see "Welcome back! 3-day streak 🔥")
2. See "For You" feed
3. Scroll through 3-5 videos
4. See interesting challenge
5. Tap "Try This Challenge"
6. Record video following guide
7. Post
8. Continue scrolling
9. Validate 2-3 peers' skills
10. Check notifications
11. See "You earned 50 XP today!"
```

**Goal:** Daily engagement, 15+ minutes in-app

---

### Flow 3: Job Seeker Journey

```
1. Build portfolio (20+ validated skills)
2. Reach Journeyman level
3. Browse jobs tab
4. See "85% match" job
5. Review job details
6. Tap "Apply with Usta Profile"
7. Profile automatically sent
8. Track application status
9. Get interview request
10. Land job! 🎉
```

**Goal:** Portfolio → job match → hire

---

### Flow 4: Master Usta Content Creation

```
1. Reach Master Usta status (5000+ XP)
2. Get "Create Challenge" permission
3. Tap "Create New Challenge"
4. Record demonstration video
5. Write recording guide (3-5 shots)
6. Add tips & common mistakes
7. Set difficulty & XP reward
8. Preview challenge
9. Publish to community
10. Watch participants complete it
11. Validate best submissions
12. Challenge trends (#1 this week!)
13. Gain followers & credibility
```

**Goal:** Ustas create quality, engaging challenges

---

## 5. Feature Specifications

### 5.1 Trending Feed (Detailed Spec)

**Screen Layout:**
```
┌─────────────────────┐
│  [Top Nav]          │
│  Trending | Follow  │
├─────────────────────┤
│                     │
│   VIDEO (9:16)      │
│   Full height       │
│   Auto-playing      │
│                     │
│                     │
│  [@username]        │
│  Challenge title    │
│  Caption...         │
│                     │
│  [❤️ 1.2K]  [✅ 47] │
│  [💬 89]    [➡️]    │
│                     │
│  [🔄 Try This]      │ ← Key CTA
└─────────────────────┘
  Swipe ↕️
```

**Interactions:**
- **Swipe up:** Next video
- **Swipe down:** Previous video
- **Tap video:** Pause/play
- **Double tap:** Like (heart animation)
- **Tap "Try This":** Start challenge
- **Tap profile:** View user profile
- **Tap challenge:** See challenge details
- **Swipe left:** Quick actions (save, share, report)

**Algorithm:**
```
For You Feed Priority:
1. Challenges in user's primary skill (50%)
2. Trending challenges across platform (25%)
3. Content from followed users (15%)
4. Recommended skills (10%)

Factors:
- User's skill level
- Engagement history
- Completion history
- Similar users' preferences
```

---

### 5.2 Challenge Recording (Detailed Spec)

**Screen Layout:**
```
┌─────────────────────┐
│  [X Close]  [? Help]│
├─────────────────────┤
│  Shot 1 of 3        │
│  ●──○──○            │
├─────────────────────┤
│                     │
│   [CAMERA VIEW]     │
│                     │
│  ┌─────────────┐    │
│  │ "Show your  │    │
│  │  setup and  │    │
│  │  materials" │    │
│  └─────────────┘    │
│                     │
│     [⏺️ 5 sec]      │
│                     │
│  Common Mistakes:   │
│  • Too far away     │
│  • Poor lighting    │
└─────────────────────┘
```

**Recording Process:**
1. Show guide for Shot 1
2. Countdown: 3, 2, 1
3. Record Shot 1 (5 seconds)
4. Auto-stop after 5 seconds
5. Preview Shot 1
6. Option to redo or continue
7. Move to Shot 2
8. Repeat for all shots
9. Final preview (all shots combined)
10. Add caption & hashtags
11. Post to challenge

**Guidance System:**
- Timer shows time remaining
- Instructions overlay (semi-transparent)
- Audio cues optional
- Visual progress bar
- Tips shown at right time

**Priority:** P0 (Critical)

---

### 5.3 Skill Validation (Detailed Spec)

**Validation Action:**
```
User watches video
    ↓
Taps ✅ "Validate" button
    ↓
Optional: Rate 1-5 stars
Optional: Leave comment
    ↓
Confirms validation
    ↓
Video creator gets notification
XP awarded to both parties
```

**Validation Rules:**
- Must watch 80% of video to validate
- Can't validate own videos
- Can validate each video once
- Limit: 100 validations/day (prevent spam)
- Usta validations = 2x weight

**Validation Display:**
```
"Validated by 47 professionals ✅"

[Show 5 validator avatars]
+ 42 more

Tap to see all validators:
- @username1 (Master Usta) ⚒️
- @username2 (Usta) 🔨
- @username3 (Journeyman) ⚙️
...
```

**Trust Score:**
- Validators' level impacts trust
- Master Usta validation = highest trust
- Multiple validations from same category = higher trust
- Diverse validators = broader skill proof

**Priority:** P0 (Critical)

---

### 5.4 XP & Level System (Detailed Spec)

**XP Mechanics:**
```
Actions → XP:
- Complete easy challenge: 10 XP
- Complete medium challenge: 25 XP
- Complete hard challenge: 50 XP
- Complete expert challenge: 100 XP
- Get validated: 2 XP per validation (max 20/video)
- Validate others: 1 XP per validation (max 100/day)
- Daily login: 5 XP
- 7-day streak: 20 XP bonus
- 30-day streak: 100 XP bonus

Multipliers:
- First-time challenge: 1.5x XP
- Perfect execution (5-star avg): 1.2x XP
- Trending challenge: 1.3x XP
```

**Level Requirements:**
```
🌱 Novice:        0-100 XP (0-10 challenges)
🔧 Apprentice:    100-500 XP (10-50 challenges)
⚙️ Journeyman:    500-2,000 XP (50-200 challenges)
🔨 Usta:          2,000-5,000 XP (200-500 challenges)
⚒️ Master Usta:   5,000+ XP + peer nomination
```

**Level Unlocks:**
```
Apprentice: Can comment on videos
Journeyman: Can post freeform videos
Usta: Can create challenges
Master Usta: Can monetize challenges
```

**Visual Display:**
```
Profile Header:
┌────────────────────┐
│  ⚙️ Journeyman     │
│  [████████──] 78%  │
│  1,847 / 2,000 XP  │
│  153 XP to Usta    │
└────────────────────┘
```

**Priority:** P0 (Critical)

---

### 5.5 Streak System (Detailed Spec)

**Streak Tracking:**
- Active if user posts OR validates daily
- Resets at midnight user's timezone
- Display prominently on profile
- Notifications to maintain

**Streak Rewards:**
```
Day 7: Bronze Streak Badge + 20 XP
Day 30: Silver Streak Badge + 100 XP
Day 90: Gold Streak Badge + 500 XP
Day 365: Diamond Streak Badge + 2000 XP
```

**Streak Protection (Premium):**
- 1 Streak Freeze per week (free users)
- 3 Streak Freezes per week (Premium)
- Streak Repair: Restore lost streak ($1.99)

**Visual:**
```
🔥 15-Day Streak!

[████████████────────] 50% to next reward

Next Milestone: Day 30
Reward: Silver Badge + 100 XP
```

**Notifications:**
```
Morning: "Start your streak! Try today's challenge 🎯"
Evening: "Don't break your 15-day streak! 🔥"
After break: "Start a new streak today! 💪"
```

**Priority:** P0 (Critical)

---

## 6. Technical Requirements

### Performance
- App launch: < 2 seconds
- Feed load: < 1 second
- Video playback start: < 500ms
- API response: < 200ms (p95)
- Offline support: Read-only mode

### Compatibility
- iOS: 14.0+
- Android: 8.0+ (API 26)
- Web: Modern browsers (last 2 versions)

### Accessibility
- VoiceOver/TalkBack support
- Screen reader friendly
- High contrast mode
- Font scaling
- Closed captions on videos

### Security
- Data encrypted at rest & in transit
- GDPR & CCPA compliant
- Content moderation (AI + human)
- User blocking/reporting
- Private data protection

---

## 7. Success Metrics

### North Star Metric
**Weekly Active Users (WAU)**
- Measures engaged user base
- Target: 70% of registered users

### Primary Metrics

**Engagement:**
- Daily Active Users (DAU): Target 40% of total users
- Time in app: Target 15+ minutes/session
- Challenges completed: Target 2+ per week per active user
- Streak maintenance: Target 30% of users with 7+ day streak

**Content:**
- Videos posted: Target 1+ per user per week
- Validation rate: Target 3+ validations per video
- Challenge participation: Target 50+ participants per trending challenge

**Growth:**
- New users: Target 20% MoM growth
- Viral coefficient: Target 1.3x
- Retention: Day 1 (60%), Day 7 (40%), Day 30 (25%)

**Monetization:**
- Premium conversion: Target 2% of active users
- Job posts: Target 1% of employers
- ARPU: Target $21 by Year 5

### Secondary Metrics

**Quality:**
- Average validation per video: 5+
- Video completion rate: 70%+
- User satisfaction (NPS): 50+

**Community:**
- Master Ustas: 100+ by Month 6
- Active challenges: 500+ live
- Cross-skill networking: 20% of follows outside primary skill

---

## 8. Non-Functional Requirements

### Reliability
- 99.9% uptime
- < 0.1% crash rate
- Graceful degradation
- Automatic failover

### Scalability
- Support 1M+ concurrent users
- Handle 10K video uploads/day
- Process videos within 2 minutes
- Serve 100M video views/month

### Data Privacy
- User controls data visibility
- Delete account = full data removal
- Export user data (GDPR)
- No selling user data

### Content Moderation
- AI screening for inappropriate content
- User reporting system
- Manual review queue
- Community guidelines enforcement

---

## 9. MVP Scope Summary

### Must Have (MVP):
✅ Trending feed (TikTok-style)  
✅ Challenge system with guided recording  
✅ User profiles & portfolios  
✅ Skill validation  
✅ XP & levels  
✅ Streaks  
✅ Follow system  
✅ Auth & onboarding  

### Nice to Have (V1.1):
- Comments
- Direct messaging
- Basic job board
- Share to social media

### Future (V2+):
- Expert courses
- Skill trees
- Advanced job matching
- Certifications
- Monetization features

---

## 10. Launch Criteria

### MVP Ready When:
- [ ] All P0 features built & tested
- [ ] App approved by App Store & Play Store
- [ ] Backend can handle 10K users
- [ ] 50+ initial challenges ready
- [ ] 25+ Master Ustas committed
- [ ] Content moderation in place
- [ ] Analytics tracking working
- [ ] Legal docs (ToS, Privacy) complete

### Beta Launch When:
- [ ] 100 beta testers recruited
- [ ] Feedback cycle established
- [ ] Major bugs fixed
- [ ] Performance targets met

### Public Launch When:
- [ ] Beta feedback incorporated
- [ ] Crash rate < 0.1%
- [ ] 500+ challenges live
- [ ] Press/marketing ready
- [ ] Support system in place

---

## 11. Risks & Dependencies

### Critical Dependencies
- AWS infrastructure setup
- Video processing pipeline
- App store approvals
- Master Usta recruitment
- Initial challenge library

### Key Risks
- **User acquisition:** Mitigate with Usta partnerships
- **Content quality:** Mitigate with validation system
- **Engagement:** Mitigate with streaks & gamification
- **Monetization timing:** Mitigate with free model first
- **Competition:** Mitigate with speed to market

---

## 12. Open Questions

### To Resolve:
1. **Launch vertical:** Start with tech, trades, or culinary?
2. **Content moderation:** Human, AI, or hybrid?
3. **Monetization timing:** Month 6 or Month 12?
4. **Web vs mobile priority:** Mobile-first or simultaneous?
5. **Internationalization:** English-only or multi-language from start?

### To Research:
1. Optimal challenge length (60s vs 90s?)
2. Validation threshold (10 or 20 for verified?)
3. XP tuning (how much per action?)
4. Streak difficulty (too easy vs too hard?)

---

## 13. Timeline

### Month 1-2: Foundation
- Set up development environment
- Configure AWS infrastructure
- Build authentication system
- Create database schema

### Month 3-4: Core Features
- Video upload & playback
- Challenge system
- Basic feed
- Profile pages

### Month 5-6: Engagement Features
- Validation system
- XP & levels
- Streaks
- Following system

### Month 6: MVP Launch
- Beta testing
- Bug fixes
- Performance optimization
- Soft launch

### Month 7-12: Growth & Iteration
- Add job board
- Add messaging
- Add comments
- Scale infrastructure
- Iterate based on data

---

## 14. Appendices

### A. User Stories (Complete List)

**As a learner, I want to:**
- Discover trending skills in my field
- Follow guided templates to record skills
- Get validated by professionals
- Track my progress and level up
- Build a portfolio automatically
- Connect with other learners

**As a Master Usta, I want to:**
- Create skill challenges for others
- Share my expertise
- Build my following
- Validate quality work
- Earn from my content
- Lead industry trends

**As an employer, I want to:**
- See candidates' real skills
- Post jobs to validated talent pool
- Find matches quickly
- Reduce hiring costs
- Access video portfolios

**As the platform, I want to:**
- Maintain high-quality content
- Foster positive community
- Enable skill validation
- Support career growth
- Generate revenue sustainably

### B. Glossary

- **Usta:** Master craftsman; highest user level
- **Challenge:** Guided skill demonstration created by Usta
- **Validation:** Peer endorsement of demonstrated skill
- **XP:** Experience points earned through activity
- **Streak:** Consecutive days of activity
- **For You:** Algorithm-driven feed
- **Following:** Feed of followed users' content

---

**PRD Status:** Draft v1.0  
**Next Review:** After team feedback  
**Approval Needed:** Founder, CTO, Design Lead  

🔨 **Ready to build Usta.**

