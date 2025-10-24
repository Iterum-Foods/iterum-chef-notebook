# 💰 USTA - Financial Model Guide

## Overview

This document provides the framework for building a detailed financial model in Excel or Google Sheets. Use this as a template to create your comprehensive 5-year financial projections.

---

## 1. Sheet Structure

### Recommended Sheets:
1. **Dashboard** - Summary & key metrics
2. **Revenue Model** - Detailed revenue projections
3. **User Growth** - User acquisition & retention
4. **Costs** - Operating expenses breakdown
5. **Unit Economics** - CAC, LTV, payback
6. **Scenarios** - Best/base/worst case
7. **Cash Flow** - Monthly cash flow
8. **Fundraising** - Rounds, dilution, cap table

---

## 2. Dashboard Sheet

### Key Metrics Display

```
┌────────────────────────────────────────────┐
│        USTA - 5-YEAR PROJECTIONS           │
├────────────────────────────────────────────┤
│                                            │
│  Year 5 Revenue:      $50.4M              │
│  Year 5 EBITDA:       $32.9M (65%)        │
│  Total Users:         2M                  │
│  MAU:                 1.4M (70%)          │
│                                            │
│  LTV/CAC:             12.6:1              │
│  Payback Period:      3 months            │
│  Gross Margin:        85%                 │
│                                            │
└────────────────────────────────────────────┘

[Revenue Chart - 5 years]
[User Growth Chart]
[EBITDA Margin Chart]
```

---

## 3. Revenue Model Sheet

### Column Structure

| Month | Users | MAU | Premium Users | Job Posts | Ad Impressions | Revenue Detail... | Total Revenue |
|-------|-------|-----|---------------|-----------|----------------|-------------------|---------------|

### Revenue Formulas

#### Job Board Revenue
```excel
= (MAU * Job_Conversion_Rate) * Avg_Job_Price

Where:
Job_Conversion_Rate = 1.5% (employers post jobs)
Avg_Job_Price = $299 (weighted average)

Example Year 1:
= (35,000 * 0.015) * 299
= 525 * 299
= $157K/year
```

#### Premium Subscription Revenue
```excel
= (MAU * Premium_Conversion_Rate) * Premium_Price * 12

Where:
Premium_Conversion_Rate = 2%
Premium_Price = $12.99/month (weighted avg)

Example Year 1:
= (35,000 * 0.02) * 12.99 * 12
= 700 * 12.99 * 12
= $109K/year
```

#### Advertising Revenue
```excel
= (MAU * Sessions_Per_Month * Videos_Per_Session * Ad_Frequency) * CPM / 1000

Where:
Sessions_Per_Month = 20
Videos_Per_Session = 15
Ad_Frequency = 1 ad per 10 videos
CPM = $10

Example Year 1:
= (35,000 * 20 * 15 * 0.1) * 10 / 1000
= 1,050,000 impressions * $10 / 1000
= $10.5K/month = $126K/year
```

#### Learning Revenue
```excel
= (Total_Users * Course_Take_Rate) * Avg_Course_Price

Where:
Course_Take_Rate = 5% (Year 3+)
Avg_Course_Price = $199

Launches Year 3
```

#### Enterprise Revenue
```excel
= Number_of_Enterprise_Clients * Avg_Contract_Value

Where:
Avg_Contract_Value = $12K/year

Launches Year 2
```

---

## 4. User Growth Sheet

### Growth Inputs

**Acquisition Channels:**
```
Month 1-6 (Pre-Product-Market-Fit):
- Usta partners: 40%
- Organic/viral: 30%
- Paid ads: 20%
- PR/press: 10%

Month 7-18 (Finding PMF):
- Viral: 50%
- Paid ads: 30%
- Usta partners: 15%
- PR: 5%

Month 19+ (Network Effects):
- Viral: 70%
- Paid ads: 20%
- Organic: 10%
```

**Growth Rates:**
```
Month 1-6: 15% MoM
Month 7-12: 25% MoM
Month 13-24: 30% MoM
Month 25-36: 20% MoM
Month 37+: 15% MoM
```

### Retention Cohorts

```
         D1    D7    D30   M2    M3    M6    M12
Cohort   60%   40%   25%   18%   15%   12%   10%

Example:
1000 users sign up in January
Day 1: 600 active
Day 7: 400 active
Day 30: 250 active
Month 2: 180 active
...
Month 12: 100 active
```

### User Calculation
```excel
New Users This Month = 
  (Paid Ads * Conversion) + 
  (Viral from existing users * Viral_Coefficient) +
  (Usta partners * followers * conversion) +
  (PR/Other sources)

Total Users = Previous Total + New Users

MAU = Total Users * Retention_Rate_for_Month

DAU = MAU * 0.4 (40% of MAU active daily)
```

---

## 5. Cost Sheet

### Cost Categories

#### Infrastructure Costs
```excel
Formula: Users * Cost_Per_User_Per_Month

Year 1: 50K users * $0.50 = $25K/month = $300K/year
Year 2: 250K users * $0.48 = $120K/month = $1.44M/year

Components:
- AWS EC2/ECS: 40%
- Database (RDS): 25%
- Video storage (S3): 20%
- CDN (CloudFront): 10%
- Other services: 5%
```

#### Personnel Costs
```excel
Role | Count | Avg Salary | Total

Year 1:
Engineers (5) * $120K = $600K
Designer (1) * $90K = $90K
Product (1) * $110K = $110K
Growth (1) * $100K = $100K
Total: $900K

Year 2: Add 8 people → $1.8M
Year 3: Add 12 people → $3.5M
```

#### Marketing Costs
```excel
= (Paid_Users * CAC) + Brand_Marketing + Events

Year 1: (10,000 * $12) + $150K + $50K = $320K
Year 2: (50,000 * $10) + $250K + $100K = $850K
```

#### Operations
```
- Office/co-working: $2K/month
- Tools & software: $5K/month
- Legal & accounting: $3K/month
- Insurance: $1K/month
- Other: $2K/month

Total: ~$150K/year
```

---

## 6. Unit Economics Sheet

### Key Formulas

#### Customer Acquisition Cost (CAC)
```excel
CAC = Total Marketing Spend / New Users Acquired

Year 1 Paid CAC = $250K / 20,000 = $12.50
Year 1 Blended CAC = $250K / 50,000 = $5.00 (includes viral)
```

#### Lifetime Value (LTV)
```excel
LTV = ARPU * Gross_Margin * (1 / Annual_Churn)

Year 5 Example:
ARPU = $25.20/year
Gross Margin = 85%
Annual Churn = 18%

LTV = $25.20 * 0.85 * (1 / 0.18) = $119

Conservative: $100
Optimistic: $150
```

#### LTV/CAC Ratio
```excel
= LTV / CAC

Target: > 3:1 (healthy)
Usta: 10-25:1 (excellent!)

Year 1: $100 / $12 = 8.3:1
Year 5: $119 / $5 = 23.8:1 (with viral)
```

#### Payback Period
```excel
= CAC / (Monthly_Revenue_Per_User * Gross_Margin)

Example:
CAC = $12
Monthly revenue = $2.10
Gross margin = 85%

Payback = $12 / ($2.10 * 0.85) = 6.7 months

Target: < 12 months
Usta: 3-7 months ✓
```

---

## 7. Scenario Planning

### Three Scenarios

#### Best Case (30% probability)
- Viral coefficient: 1.5x
- Premium conversion: 3%
- User growth: 35% MoM
- **Year 5:** 3M users, $75M revenue

#### Base Case (50% probability)
- Viral coefficient: 1.3x
- Premium conversion: 2%
- User growth: 25% MoM
- **Year 5:** 2M users, $50M revenue

#### Worst Case (20% probability)
- Viral coefficient: 1.1x
- Premium conversion: 1%
- User growth: 15% MoM
- **Year 5:** 800K users, $20M revenue

### Sensitivity Analysis

**What if... Premium conversion is 1% instead of 2%?**
- Revenue impact: -$9M in Year 5
- Mitigation: Increase job board focus

**What if... CAC is $20 instead of $12?**
- Need more capital
- Focus on viral growth
- Slower user acquisition

**What if... Retention drops to D30: 15%?**
- MAU decreases 40%
- Revenue drops proportionally
- Fix: Improve product engagement

---

## 8. Cash Flow Management

### Monthly Cash Flow

```
Beginning Cash
+ Revenue (collected)
- Infrastructure costs
- Payroll
- Marketing spend
- Operating expenses
= Ending Cash

Track:
- Burn rate
- Runway (months)
- Cash balance
```

### Runway Calculation
```excel
Runway (months) = Cash_Balance / Monthly_Burn_Rate

Example:
$1.5M raised
$75K/month burn (after revenue)

Runway = $1,500,000 / $75,000 = 20 months
```

### Capital Requirements
```
Seed Round: $1.5M (Month 0)
→ 18-month runway
→ Hit Series A metrics

Series A: $10M (Month 18)
→ 24-month runway
→ Hit profitability

Series B: $30M (Month 42)
→ Scale internationally
→ Market leadership
```

---

## 9. Key Assumptions

### User Assumptions
```excel
Signups to MAU: 70%
MAU to DAU: 40%
Viral Coefficient: 1.3x
Activation Rate: 60%
Annual Churn: 18%
```

### Revenue Assumptions
```excel
Premium Conversion: 2% of MAU
Job Post Conversion: 1.5% of employers (0.3% of users)
Ad CPM: $10
Course Take Rate: 5% (Year 3+)
```

### Cost Assumptions
```excel
Infrastructure: $0.50/user/month (scales down to $0.40)
Salary Growth: 5% per year
Marketing CAC: $12 (paid), $0 (viral)
Gross Margin: 85%
```

---

## 10. Valuation Framework

### Comparable Companies (Public)

| Company | Revenue | Valuation | Multiple |
|---------|---------|-----------|----------|
| Duolingo | $500M | $7B | 14x |
| LinkedIn | $15B | $27B (at acquisition) | 1.8x |
| Fiverr | $350M | $2.5B | 7x |
| Upwork | $600M | $1.8B | 3x |

### Comparable Startups (Private)

| Company | Stage | Valuation | Revenue | Multiple |
|---------|-------|-----------|---------|----------|
| Masterclass | Series F | $2.75B | $200M | 13.8x |
| Handshake | Series F | $3.5B | $150M | 23x |
| Coursera | IPO | $5B | $400M | 12.5x |

### Usta Valuation (Projected)

**At $500K ARR (Seed Exit):**
- Revenue multiple: 15-20x (early stage)
- Valuation: $7.5M-10M
- Our raise: $1.5M at $8M pre = reasonable

**At $10M ARR (Series A):**
- Revenue multiple: 10-15x
- Valuation: $100M-150M

**At $50M ARR (Series B/Exit):**
- Revenue multiple: 8-12x
- Valuation: $400M-600M

**At Scale (IPO/Strategic):**
- 2M+ users, $50M+ revenue
- Multiple: 10-20x depending on growth
- Valuation: $500M-$2B range

---

## 11. Burn Rate & Runway

### Monthly Burn Calculation

```excel
Month 6 Example:

Revenue:           $25K
Costs:
  Infrastructure:  -$2.5K
  Payroll:        -$75K
  Marketing:      -$30K
  Operations:     -$7K
Total Costs:      -$114.5K

Net Burn:         -$89.5K/month
```

### Runway Table
```
Starting Cash: $1,500,000

Month  Revenue  Costs   Burn    Remaining
1      $5K      -$95K   -$90K   $1,410K
2      $8K      -$98K   -$90K   $1,320K
3      $12K     -$100K  -$88K   $1,232K
...
18     $185K    -$215K  -$30K   $220K  ← Series A needed
```

---

## 12. Break-Even Analysis

### Break-Even Formula
```excel
Break-Even Users = Fixed_Costs / (Revenue_Per_User - Variable_Cost_Per_User)

Example:
Fixed Costs = $150K/month (team, office)
Revenue Per User = $2.10/month
Variable Cost = $0.50/month (infrastructure)

Break-Even = $150,000 / ($2.10 - $0.50)
           = $150,000 / $1.60
           = 93,750 users

At 70% MAU rate = 134,000 total users needed
```

### Path to Profitability
```
Month 28: First profitable month
- 400K total users
- 280K MAU
- $700K revenue
- $650K costs
- $50K profit
```

---

## 13. Cohort Analysis

### Revenue by Cohort

```excel
Jan 2026 Cohort (1000 users):

Month 1:  $0 (free)
Month 2:  $200 (20 convert to premium)
Month 3:  $180 (churn)
...
Month 12: $150
Month 24: $120 (cumulative churn)

Lifetime Value = Sum of all months
```

### Retention Impact

```
Improve D30 retention from 25% → 30%:
- 20% more MAU
- 20% more revenue
- Same CAC
- 20% better LTV/CAC

Small retention improvements = huge impact!
```

---

## 14. Funding Rounds

### Seed Round (Month 0)
```
Raise: $1.5M
Pre-money: $8M
Post-money: $9.5M
Equity: 15.8%
Investors: Angels, micro-VCs
```

### Series A (Month 18)
```
Raise: $10M
Pre-money: $40M
Post-money: $50M
Equity: 20%
Investors: Traditional VCs

Metrics needed:
- 100K users
- $1M ARR
- 30%+ MoM growth
- Strong unit economics
```

### Series B (Month 36)
```
Raise: $30M
Pre-money: $170M
Post-money: $200M
Equity: 15%

Metrics needed:
- 1M users
- $15M ARR
- Path to profitability
- International presence
```

---

## 15. Cap Table Evolution

### Post-Seed
```
Founders:          70%
Angels/Seed:       16%
Employee Pool:     14%
Total:            100%
```

### Post-Series A
```
Founders:          56%  (diluted)
Angels/Seed:       12.8% (diluted)
Series A:          20%
Employee Pool:     11.2%
Total:            100%
```

### Post-Series B
```
Founders:          47.6%
Angels/Seed:       10.9%
Series A:          17%
Series B:          15%
Employee Pool:     9.5%
Total:            100%
```

---

## 16. Key Metrics to Track

### Growth Metrics
- Total Users
- New Users (MoM)
- Growth Rate (%)
- MAU
- DAU
- WAU

### Engagement Metrics
- Time in app
- Videos watched per session
- Challenges completed
- Validations given
- Streak maintenance rate

### Monetization Metrics
- ARPU (Average Revenue Per User)
- Premium conversion rate
- Job post conversion
- Ad CPM
- Course completion rate

### Health Metrics
- CAC (by channel)
- LTV
- LTV/CAC ratio
- Payback period
- Churn rate
- Net revenue retention

---

## 17. Financial Model Checklist

### Build Phase
- [ ] Set up sheet structure
- [ ] Input all assumptions (documented)
- [ ] Build revenue formulas
- [ ] Build cost formulas
- [ ] Link everything to dashboard
- [ ] Create charts/visualizations
- [ ] Build scenario analysis
- [ ] Add sensitivity tables

### Review Phase
- [ ] Sanity check all numbers
- [ ] Compare to comparables
- [ ] Stress test assumptions
- [ ] Review with advisors
- [ ] Get accountant review
- [ ] Update based on feedback

### Use Phase
- [ ] Share with investors (view-only)
- [ ] Update monthly with actuals
- [ ] Compare actual vs projected
- [ ] Adjust future projections
- [ ] Track variance
- [ ] Report to board

---

## 18. Critical Formulas Summary

```excel
// Revenue
Total_Revenue = Job_Board + Premium + Ads + Learning + Enterprise

// Costs
Total_Costs = Infrastructure + Personnel + Marketing + Operations

// Profitability
EBITDA = Total_Revenue - Total_Costs
EBITDA_Margin = EBITDA / Total_Revenue

// Users
MAU = Total_Users * Retention_Rate
DAU = MAU * 0.4

// Unit Economics
CAC = Marketing_Spend / New_Users
LTV = ARPU * Gross_Margin / Churn_Rate
Payback = CAC / (Monthly_Revenue_Per_User * Gross_Margin)

// Cash
Burn_Rate = (Costs - Revenue) / Month
Runway = Cash_Balance / Burn_Rate
```

---

## 19. Templates to Use

### Excel/Google Sheets
**Recommended:** Start with Google Sheets for collaboration

**Template Sources:**
- YCombinator's financial model template
- Visible.vc financial model
- Carta's startup templates
- Causal.app (financial modeling tool)

### Financial Modeling Tools
- **Causal:** Modern, collaborative
- **Runway:** Financial planning for startups
- **Google Sheets:** Free, accessible
- **Excel:** Most professional investors prefer

---

## 20. Reporting Cadence

### Internal (Team)
- **Daily:** User growth, engagement
- **Weekly:** Revenue, key metrics
- **Monthly:** Full P&L review
- **Quarterly:** Board presentation

### External (Investors)
- **Monthly:** Email update with key metrics
- **Quarterly:** Detailed financial review
- **Annually:** Strategic planning session

### Metrics to Report
```
Subject: Usta Monthly Update - October 2025

Key Metrics:
- Users: 47K (+18% MoM)
- MAU: 32K (68% of total)
- Revenue: $28K (+22% MoM)
- Burn: $85K/month
- Runway: 16 months

Wins:
- Launched #WeldingBasics (2.8K participants!)
- 3 new Master Ustas signed
- Featured in WeldingTips magazine

Challenges:
- D30 retention at 23% (target 25%)
- Working on improved onboarding

Ask:
- Intro to [specific investor]
```

---

## Conclusion

A solid financial model is critical for:
- **Planning:** Know when you'll run out of money
- **Fundraising:** Show investors the opportunity
- **Decision-making:** Hire? Spend on marketing? Pivot?
- **Accountability:** Track actual vs projected

**Build it once, update it monthly, use it constantly.**

---

**Model Status:** Template provided  
**Next Step:** Build in Google Sheets  
**Owner:** Founder + Finance Team  
**Review:** Monthly  

🔨 **Numbers drive decisions.**

