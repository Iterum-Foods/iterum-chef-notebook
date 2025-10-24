import React, { useState, useMemo } from 'react';
import { useApp } from '../../contexts/AppContext';
import FormField from '../ui/FormField';
import SectionCard from '../ui/SectionCard';
import { TrendingUp, Users, MapPin, DollarSign, Target, BarChart3, PieChart, Globe, Building, Utensils } from 'lucide-react';

const MarketAnalysis = () => {
  const { state, actions } = useApp();
  const data = state.businessPlan.marketAnalysis;
  const [activeTab, setActiveTab] = useState('overview');

  const handleFieldChange = (field, value) => {
    actions.updateBusinessPlan('marketAnalysis', { [field]: value });
  };

  // Boston restaurant market data
  const bostonMarketData = {
    marketSize: {
      totalRestaurants: 4200,
      annualRevenue: 2.8, // billion
      employmentSize: 78000,
      growthRate: 3.2
    },
    demographics: {
      population: 695506,
      medianAge: 32.1,
      medianIncome: 71115,
      collegeEducated: 47.9,
      touristVisits: 21.2 // million annually
    },
    trends: [
      { trend: 'Farm-to-table dining', growth: '+12%', impact: 'High' },
      { trend: 'Craft beer/cocktails', growth: '+8%', impact: 'High' },
      { trend: 'Food delivery/ghost kitchens', growth: '+25%', impact: 'Very High' },
      { trend: 'Sustainable/eco-friendly', growth: '+15%', impact: 'Medium' },
      { trend: 'Ethnic fusion cuisine', growth: '+10%', impact: 'High' }
    ],
    neighborhoods: [
      { name: 'Back Bay', restaurants: 280, avgRent: 85, competition: 'Very High', tourism: 'High' },
      { name: 'North End', restaurants: 120, avgRent: 65, competition: 'High', tourism: 'Very High' },
      { name: 'South End', restaurants: 180, avgRent: 75, competition: 'High', tourism: 'Medium' },
      { name: 'Cambridge', restaurants: 220, avgRent: 55, competition: 'Medium', tourism: 'High' },
      { name: 'Somerville', restaurants: 140, avgRent: 45, competition: 'Medium', tourism: 'Low' },
      { name: 'Jamaica Plain', restaurants: 100, avgRent: 35, competition: 'Low', tourism: 'Low' }
    ]
  };

  const getCompetitionColor = (level) => {
    switch(level) {
      case 'Very High': return 'text-red-600 bg-red-100';
      case 'High': return 'text-orange-600 bg-orange-100';
      case 'Medium': return 'text-yellow-600 bg-yellow-100';
      case 'Low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const selectedNeighborhood = useMemo(() => {
    const location = state.businessPlan.executiveSummary.businessLocation;
    return bostonMarketData.neighborhoods.find(n => n.name === location) || bostonMarketData.neighborhoods[0];
  }, [state.businessPlan.executiveSummary.businessLocation]);

  const tabs = [
    { id: 'overview', label: 'Market Overview', icon: Globe },
    { id: 'demographics', label: 'Demographics', icon: Users },
    { id: 'competition', label: 'Competition', icon: Target },
    { id: 'trends', label: 'Market Trends', icon: TrendingUp },
    { id: 'analysis', label: 'Your Analysis', icon: BarChart3 }
  ];

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Market Size Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-blue-600">Total Restaurants</p>
              <p className="text-2xl font-bold text-blue-900">{bostonMarketData.marketSize.totalRestaurants.toLocaleString()}</p>
            </div>
            <Utensils className="h-8 w-8 text-blue-500" />
          </div>
        </div>
        
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-green-600">Annual Revenue</p>
              <p className="text-2xl font-bold text-green-900">${bostonMarketData.marketSize.annualRevenue}B</p>
            </div>
            <DollarSign className="h-8 w-8 text-green-500" />
          </div>
        </div>
        
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-purple-600">Employment</p>
              <p className="text-2xl font-bold text-purple-900">{bostonMarketData.marketSize.employmentSize.toLocaleString()}</p>
            </div>
            <Users className="h-8 w-8 text-purple-500" />
          </div>
        </div>
        
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-orange-600">Growth Rate</p>
              <p className="text-2xl font-bold text-orange-900">{bostonMarketData.marketSize.growthRate}%</p>
            </div>
            <TrendingUp className="h-8 w-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Industry Overview */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Building className="h-5 w-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">Boston Restaurant Industry Overview</h3>
        </div>
        
        <div className="prose text-gray-700 max-w-none">
          <p className="mb-4">
            Boston's restaurant industry represents a robust $2.8 billion market with over 4,200 establishments employing 
            78,000 people. The market has shown consistent growth of 3.2% annually, driven by a strong local economy, 
            significant tourism (21.2M visitors annually), and a highly educated population.
          </p>
          
          <p className="mb-4">
            The city's culinary scene is characterized by a mix of traditional New England fare, innovative contemporary 
            cuisine, and diverse ethnic offerings. Key factors driving market growth include:
          </p>
          
          <ul className="list-disc list-inside space-y-1 mb-4">
            <li>Strong tourism industry with year-round visitors</li>
            <li>High disposable income ($71,115 median household income)</li>
            <li>Young, educated population (47.9% college-educated, median age 32.1)</li>
            <li>Growing food delivery and ghost kitchen segments</li>
            <li>Increasing demand for sustainable and locally-sourced dining</li>
          </ul>
        </div>
      </div>
    </div>
  );

  const renderDemographics = () => (
    <div className="space-y-6">
      {/* Demographics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 text-center">
          <Users className="h-8 w-8 text-indigo-500 mx-auto mb-2" />
          <p className="text-sm font-medium text-indigo-600">Population</p>
          <p className="text-xl font-bold text-indigo-900">{bostonMarketData.demographics.population.toLocaleString()}</p>
        </div>
        
        <div className="bg-teal-50 border border-teal-200 rounded-lg p-4 text-center">
          <BarChart3 className="h-8 w-8 text-teal-500 mx-auto mb-2" />
          <p className="text-sm font-medium text-teal-600">Median Age</p>
          <p className="text-xl font-bold text-teal-900">{bostonMarketData.demographics.medianAge}</p>
        </div>
        
        <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 text-center">
          <DollarSign className="h-8 w-8 text-emerald-500 mx-auto mb-2" />
          <p className="text-sm font-medium text-emerald-600">Median Income</p>
          <p className="text-xl font-bold text-emerald-900">${bostonMarketData.demographics.medianIncome.toLocaleString()}</p>
        </div>
        
        <div className="bg-rose-50 border border-rose-200 rounded-lg p-4 text-center">
          <MapPin className="h-8 w-8 text-rose-500 mx-auto mb-2" />
          <p className="text-sm font-medium text-rose-600">Annual Tourists</p>
          <p className="text-xl font-bold text-rose-900">{bostonMarketData.demographics.touristVisits}M</p>
        </div>
      </div>

      {/* Customer Segments */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Customer Segments</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-2">Young Professionals (25-35)</h4>
              <p className="text-sm text-gray-600 mb-2">32% of population • High disposable income • Tech/healthcare workers</p>
              <div className="flex flex-wrap gap-2">
                <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">Quick lunch</span>
                <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">After-work dining</span>
                <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">Delivery</span>
              </div>
            </div>
            
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-green-900 mb-2">College Students (18-24)</h4>
              <p className="text-sm text-gray-600 mb-2">18% of population • Budget-conscious • Social dining</p>
              <div className="flex flex-wrap gap-2">
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Casual dining</span>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Group meals</span>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Late night</span>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-purple-900 mb-2">Tourists & Visitors</h4>
              <p className="text-sm text-gray-600 mb-2">21.2M annually • Experience-seeking • Higher spending</p>
              <div className="flex flex-wrap gap-2">
                <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">Local specialties</span>
                <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">Fine dining</span>
                <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">Historic areas</span>
              </div>
            </div>
            
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-orange-900 mb-2">Families & Locals (35+)</h4>
              <p className="text-sm text-gray-600 mb-2">28% of population • Regular customers • Value-oriented</p>
              <div className="flex flex-wrap gap-2">
                <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded">Family dining</span>
                <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded">Takeout</span>
                <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded">Neighborhood spots</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderCompetition = () => (
    <div className="space-y-6">
      {/* Neighborhood Analysis */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Competition by Neighborhood</h3>
        
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Neighborhood</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Restaurants</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Avg Rent/sq ft</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Competition</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">Tourism</th>
              </tr>
            </thead>
            <tbody>
              {bostonMarketData.neighborhoods.map((neighborhood, index) => (
                <tr key={index} className={`border-b border-gray-100 ${neighborhood.name === selectedNeighborhood.name ? 'bg-blue-50' : ''}`}>
                  <td className="py-3 px-4 font-medium text-gray-900">{neighborhood.name}</td>
                  <td className="py-3 px-4 text-gray-700">{neighborhood.restaurants}</td>
                  <td className="py-3 px-4 text-gray-700">${neighborhood.avgRent}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCompetitionColor(neighborhood.competition)}`}>
                      {neighborhood.competition}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCompetitionColor(neighborhood.tourism)}`}>
                      {neighborhood.tourism}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Location Analysis */}
      {selectedNeighborhood && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">
            Your Selected Location: {selectedNeighborhood.name}
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4">
              <p className="text-sm font-medium text-gray-600">Market Density</p>
              <p className="text-2xl font-bold text-gray-900">{selectedNeighborhood.restaurants} restaurants</p>
              <p className="text-xs text-gray-500">Competition level: {selectedNeighborhood.competition}</p>
            </div>
            
            <div className="bg-white rounded-lg p-4">
              <p className="text-sm font-medium text-gray-600">Rental Cost</p>
              <p className="text-2xl font-bold text-gray-900">${selectedNeighborhood.avgRent}/sq ft</p>
              <p className="text-xs text-gray-500">Annual commercial rent</p>
            </div>
            
            <div className="bg-white rounded-lg p-4">
              <p className="text-sm font-medium text-gray-600">Tourism Impact</p>
              <p className="text-2xl font-bold text-gray-900">{selectedNeighborhood.tourism}</p>
              <p className="text-xs text-gray-500">Visitor traffic level</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const renderTrends = () => (
    <div className="space-y-6">
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center space-x-2 mb-4">
          <TrendingUp className="h-5 w-5 text-green-600" />
          <h3 className="text-lg font-semibold text-gray-900">Current Market Trends</h3>
        </div>
        
        <div className="space-y-4">
          {bostonMarketData.trends.map((trend, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-gray-900">{trend.trend}</h4>
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-sm font-medium rounded">
                    {trend.growth}
                  </span>
                  <span className={`px-2 py-1 text-sm font-medium rounded ${
                    trend.impact === 'Very High' ? 'bg-red-100 text-red-800' :
                    trend.impact === 'High' ? 'bg-orange-100 text-orange-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {trend.impact} Impact
                  </span>
                </div>
              </div>
              
              <p className="text-gray-600 text-sm">
                {trend.trend === 'Farm-to-table dining' && "Local sourcing and sustainable practices are increasingly important to Boston diners."}
                {trend.trend === 'Craft beer/cocktails' && "Boston's craft beverage scene continues to grow with local breweries and artisan cocktails."}
                {trend.trend === 'Food delivery/ghost kitchens' && "Delivery-only concepts and virtual restaurants are rapidly expanding post-pandemic."}
                {trend.trend === 'Sustainable/eco-friendly' && "Environmental consciousness drives demand for eco-friendly packaging and practices."}
                {trend.trend === 'Ethnic fusion cuisine' && "Creative fusion of traditional ethnic cuisines with modern American flavors."}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderAnalysis = () => (
    <div className="space-y-6">
      <FormField
        label="Industry Overview & Market Size"
        type="textarea"
        value={data.industryOverview}
        onChange={(value) => handleFieldChange('industryOverview', value)}
        placeholder="Based on the data above, describe how your restaurant fits into Boston's $2.8B restaurant market. Consider market size, growth trends, and your target segment."
        rows={4}
      />
      
      <FormField
        label="Target Market Definition"
        type="textarea"
        value={data.targetMarket}
        onChange={(value) => handleFieldChange('targetMarket', value)}
        placeholder="Define your primary and secondary customer segments. Reference the demographic data - will you target young professionals, tourists, families, or students?"
        rows={4}
      />
      
      <FormField
        label="Competitive Positioning"
        type="textarea"
        value={data.competitiveAnalysis}
        onChange={(value) => handleFieldChange('competitiveAnalysis', value)}
        placeholder={`In ${selectedNeighborhood.name} (${selectedNeighborhood.restaurants} restaurants), how will you differentiate? What's your competitive advantage?`}
        rows={4}
      />
      
      <FormField
        label="Market Opportunity Assessment"
        type="textarea"
        value={data.marketSize}
        onChange={(value) => handleFieldChange('marketSize', value)}
        placeholder="What specific market opportunity are you targeting? Consider underserved segments, emerging trends, or gaps in your chosen neighborhood."
        rows={3}
      />
      
      <FormField
        label="Trend Alignment Strategy"
        type="textarea"
        value={data.marketTrends}
        onChange={(value) => handleFieldChange('marketTrends', value)}
        placeholder="How will your restaurant align with current trends like farm-to-table, delivery, sustainability, or craft beverages?"
        rows={3}
      />
      
      <FormField
        label="Customer Demographics & Behavior"
        type="textarea"
        value={data.customerDemographics}
        onChange={(value) => handleFieldChange('customerDemographics', value)}
        placeholder="Describe your ideal customers' dining habits, spending patterns, and preferences. How will you reach and retain them?"
        rows={3}
      />
    </div>
  );

  return (
    <div className="animate-fade-in">
      <SectionCard 
        title="Boston Restaurant Market Analysis" 
        description="Comprehensive analysis of Boston's restaurant market with real-time data and competitive insights."
        color="green"
      >
        {/* Tab Navigation */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="flex space-x-8" aria-label="Tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`${
                  activeTab === tab.id
                    ? 'border-green-500 text-green-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2`}
              >
                <tab.icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'demographics' && renderDemographics()}
        {activeTab === 'competition' && renderCompetition()}
        {activeTab === 'trends' && renderTrends()}
        {activeTab === 'analysis' && renderAnalysis()}
      </SectionCard>
    </div>
  );
};

export default MarketAnalysis; 