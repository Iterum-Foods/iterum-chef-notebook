import React, { useState, useMemo } from 'react';
import { useApp } from '../../contexts/AppContext';
import SectionCard from '../ui/SectionCard';
import { 
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  TrendingUp, TrendingDown, DollarSign, Users, Target, 
  BarChart3, Activity, AlertCircle 
} from 'lucide-react';

const BusinessAnalytics = () => {
  const { state } = useApp();
  const [selectedTimeframe, setSelectedTimeframe] = useState('12months');

  const financialData = state.businessPlan.financialProjections;

  // Generate financial projections data for charts
  const projectionData = useMemo(() => {
    if (!financialData) return [];
    
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    const baseRevenue = parseInt(financialData.projectedRevenue) || 300000;
    const baseCosts = parseInt(financialData.operatingExpenses) || 180000;
    
    return months.map((month, index) => {
      // Add seasonal variation for restaurants
      const seasonalMultiplier = month === 'Dec' ? 1.3 : 
                                month === 'Nov' ? 1.2 :
                                month === 'Jan' ? 0.8 :
                                month === 'Feb' ? 0.9 : 1.0;
      
      const monthlyRevenue = Math.round((baseRevenue / 12) * seasonalMultiplier);
      const monthlyCosts = Math.round((baseCosts / 12) * (0.9 + Math.random() * 0.2));
      const profit = monthlyRevenue - monthlyCosts;
      
      return {
        month,
        revenue: monthlyRevenue,
        costs: monthlyCosts,
        profit: profit,
        grossMargin: Math.round((profit / monthlyRevenue) * 100),
        customers: Math.round((monthlyRevenue / 45) * seasonalMultiplier), // Avg $45 per customer
        avgOrderValue: Math.round(monthlyRevenue / (monthlyRevenue / 45))
      };
    });
  }, [financialData]);

  // Key performance indicators
  const kpis = useMemo(() => {
    if (!projectionData.length) return {};
    
    const totalRevenue = projectionData.reduce((sum, month) => sum + month.revenue, 0);
    const totalCosts = projectionData.reduce((sum, month) => sum + month.costs, 0);
    const totalProfit = totalRevenue - totalCosts;
    const avgMargin = Math.round((totalProfit / totalRevenue) * 100);
    const totalCustomers = projectionData.reduce((sum, month) => sum + month.customers, 0);
    const avgOrderValue = Math.round(totalRevenue / totalCustomers);
    
    // Compare to Boston restaurant benchmarks
    const benchmarks = {
      grossMargin: 28, // Industry average for restaurants
      customerGrowth: 15, // Annual growth rate
      avgOrderValue: 45 // Boston restaurant average
    };
    
    return {
      totalRevenue,
      totalCosts,
      totalProfit,
      avgMargin,
      totalCustomers,
      avgOrderValue,
      benchmarks,
      performance: {
        marginVsBenchmark: avgMargin - benchmarks.grossMargin,
        aovVsBenchmark: avgOrderValue - benchmarks.avgOrderValue
      }
    };
  }, [projectionData]);

  // Market position data
  const marketData = [
    { category: 'Fine Dining', share: 15, competitors: 120, avgPrice: 85 },
    { category: 'Casual Dining', share: 35, competitors: 280, avgPrice: 45 },
    { category: 'Fast Casual', share: 25, competitors: 200, avgPrice: 25 },
    { category: 'Quick Service', share: 20, competitors: 150, avgPrice: 15 },
    { category: 'Specialty', share: 5, competitors: 50, avgPrice: 35 }
  ];

  // Cost breakdown data
  const costBreakdown = [
    { category: 'Food Cost', amount: parseInt(financialData?.foodCosts) || 90000, percentage: 30, color: '#8884d8' },
    { category: 'Labor', amount: parseInt(financialData?.salaries) || 72000, percentage: 24, color: '#82ca9d' },
    { category: 'Rent', amount: parseInt(financialData?.rent) || 48000, percentage: 16, color: '#ffc658' },
    { category: 'Utilities', amount: parseInt(financialData?.utilities) || 18000, percentage: 6, color: '#ff7300' },
    { category: 'Marketing', amount: parseInt(financialData?.marketing) || 15000, percentage: 5, color: '#00ff88' },
    { category: 'Other', amount: parseInt(financialData?.otherExpenses) || 27000, percentage: 9, color: '#ff8088' }
  ];

  const timeframes = [
    { id: '3months', label: '3 Months' },
    { id: '6months', label: '6 Months' },
    { id: '12months', label: '12 Months' },
    { id: '24months', label: '2 Years' }
  ];

  const metrics = [
    { id: 'revenue', label: 'Revenue', icon: DollarSign, color: 'green' },
    { id: 'profit', label: 'Profit', icon: TrendingUp, color: 'blue' },
    { id: 'customers', label: 'Customers', icon: Users, color: 'purple' },
    { id: 'margin', label: 'Gross Margin', icon: BarChart3, color: 'orange' }
  ];

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('en-US').format(value);
  };

  return (
    <div className="animate-fade-in space-y-6">
      {/* KPI Dashboard */}
      <SectionCard 
        title="Key Performance Indicators" 
        description="Essential metrics for your restaurant's financial health and performance."
        color="blue"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-gradient-to-r from-green-50 to-green-100 border border-green-200 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">Annual Revenue</p>
                <p className="text-2xl font-bold text-green-900">{formatCurrency(kpis.totalRevenue)}</p>
                <p className="text-xs text-green-600 mt-1">Projected for Year 1</p>
              </div>
              <DollarSign className="h-8 w-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-blue-50 to-blue-100 border border-blue-200 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600">Net Profit</p>
                <p className="text-2xl font-bold text-blue-900">{formatCurrency(kpis.totalProfit)}</p>
                <div className="flex items-center mt-1">
                  {kpis.performance?.marginVsBenchmark > 0 ? (
                    <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
                  )}
                  <p className="text-xs text-blue-600">
                    {Math.abs(kpis.performance?.marginVsBenchmark)}% vs benchmark
                  </p>
                </div>
              </div>
              <BarChart3 className="h-8 w-8 text-blue-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-purple-50 to-purple-100 border border-purple-200 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-600">Expected Customers</p>
                <p className="text-2xl font-bold text-purple-900">{formatNumber(kpis.totalCustomers)}</p>
                <p className="text-xs text-purple-600 mt-1">Annual visits</p>
              </div>
              <Users className="h-8 w-8 text-purple-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-orange-50 to-orange-100 border border-orange-200 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600">Avg Order Value</p>
                <p className="text-2xl font-bold text-orange-900">{formatCurrency(kpis.avgOrderValue)}</p>
                <div className="flex items-center mt-1">
                  {kpis.performance?.aovVsBenchmark > 0 ? (
                    <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
                  )}
                  <p className="text-xs text-orange-600">
                    {formatCurrency(Math.abs(kpis.performance?.aovVsBenchmark))} vs benchmark
                  </p>
                </div>
              </div>
              <Target className="h-8 w-8 text-orange-500" />
            </div>
          </div>
        </div>
      </SectionCard>

      {/* Financial Projections Chart */}
      <SectionCard 
        title="Financial Projections" 
        description="Monthly revenue, costs, and profit projections with seasonal variations."
        color="green"
      >
        <div className="mb-4 flex flex-wrap gap-4">
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium text-gray-700">Timeframe:</span>
            {timeframes.map(timeframe => (
              <button
                key={timeframe.id}
                onClick={() => setSelectedTimeframe(timeframe.id)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  selectedTimeframe === timeframe.id
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {timeframe.label}
              </button>
            ))}
          </div>
        </div>
        
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={projectionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis tickFormatter={(value) => `$${value/1000}k`} />
              <Tooltip 
                formatter={(value) => [formatCurrency(value), '']}
                labelFormatter={(label) => `Month: ${label}`}
              />
              <Legend />
              <Area 
                type="monotone" 
                dataKey="revenue" 
                stackId="1" 
                stroke="#10b981" 
                fill="#10b981" 
                fillOpacity={0.6}
                name="Revenue"
              />
              <Area 
                type="monotone" 
                dataKey="costs" 
                stackId="2" 
                stroke="#ef4444" 
                fill="#ef4444" 
                fillOpacity={0.6}
                name="Costs"
              />
              <Line 
                type="monotone" 
                dataKey="profit" 
                stroke="#3b82f6" 
                strokeWidth={3}
                name="Profit"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Cost Breakdown */}
        <SectionCard 
          title="Cost Breakdown" 
          description="Operating expense distribution for your restaurant."
          color="orange"
        >
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={costBreakdown}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="amount"
                >
                  {costBreakdown.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => formatCurrency(value)} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          
          <div className="mt-4 space-y-2">
            {costBreakdown.map((item, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-gray-700">{item.category}</span>
                </div>
                <div className="text-right">
                  <span className="font-medium">{formatCurrency(item.amount)}</span>
                  <span className="text-gray-500 ml-2">({item.percentage}%)</span>
                </div>
              </div>
            ))}
          </div>
        </SectionCard>

        {/* Market Position */}
        <SectionCard 
          title="Boston Market Position" 
          description="Your restaurant category within Boston's dining landscape."
          color="purple"
        >
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={marketData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="category" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => {
                    if (name === 'share') return [`${value}%`, 'Market Share'];
                    if (name === 'competitors') return [value, 'Competitors'];
                    if (name === 'avgPrice') return [formatCurrency(value), 'Avg Price'];
                    return [value, name];
                  }}
                />
                <Legend />
                <Bar dataKey="share" fill="#8884d8" name="Market Share %" />
                <Bar dataKey="competitors" fill="#82ca9d" name="Competitors" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-900 mb-2">Market Insights</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Casual dining dominates with 35% market share</li>
              <li>• 850+ total restaurants competing in Boston</li>
              <li>• Average prices range from $15-$85 per person</li>
              <li>• Specialty concepts show growth potential</li>
            </ul>
          </div>
        </SectionCard>
      </div>

      {/* Performance Benchmarks */}
      <SectionCard 
        title="Performance vs. Industry Benchmarks" 
        description="How your projections compare to Boston restaurant industry standards."
        color="indigo"
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-gray-900">Gross Margin</h4>
              {kpis.performance?.marginVsBenchmark > 0 ? (
                <TrendingUp className="h-5 w-5 text-green-500" />
              ) : (
                <TrendingDown className="h-5 w-5 text-red-500" />
              )}
            </div>
            
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Your Restaurant</span>
                  <span className="font-medium">{kpis.avgMargin}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${Math.min(kpis.avgMargin * 2, 100)}%` }}
                  ></div>
                </div>
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Industry Average</span>
                  <span className="font-medium">{kpis.benchmarks?.grossMargin}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gray-400 h-2 rounded-full"
                    style={{ width: `${Math.min(kpis.benchmarks?.grossMargin * 2, 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
            
            <p className="text-xs text-gray-600 mt-3">
              {kpis.performance?.marginVsBenchmark > 0 
                ? `${kpis.performance.marginVsBenchmark}% above industry average`
                : `${Math.abs(kpis.performance?.marginVsBenchmark)}% below industry average`
              }
            </p>
          </div>

          <div className="border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-gray-900">Average Order Value</h4>
              {kpis.performance?.aovVsBenchmark > 0 ? (
                <TrendingUp className="h-5 w-5 text-green-500" />
              ) : (
                <TrendingDown className="h-5 w-5 text-red-500" />
              )}
            </div>
            
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Your Restaurant</span>
                  <span className="font-medium">{formatCurrency(kpis.avgOrderValue)}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: `${Math.min((kpis.avgOrderValue / 100) * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Boston Average</span>
                  <span className="font-medium">{formatCurrency(kpis.benchmarks?.avgOrderValue)}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gray-400 h-2 rounded-full"
                    style={{ width: `${Math.min((kpis.benchmarks?.avgOrderValue / 100) * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
            
            <p className="text-xs text-gray-600 mt-3">
              {kpis.performance?.aovVsBenchmark > 0 
                ? `${formatCurrency(kpis.performance.aovVsBenchmark)} above Boston average`
                : `${formatCurrency(Math.abs(kpis.performance?.aovVsBenchmark))} below Boston average`
              }
            </p>
          </div>

          <div className="border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-gray-900">Key Ratios</h4>
              <Activity className="h-5 w-5 text-blue-500" />
            </div>
            
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span>Food Cost %</span>
                <span className="font-medium">30%</span>
              </div>
              <div className="flex justify-between">
                <span>Labor Cost %</span>
                <span className="font-medium">24%</span>
              </div>
              <div className="flex justify-between">
                <span>Rent to Revenue</span>
                <span className="font-medium">16%</span>
              </div>
              <div className="flex justify-between">
                <span>Marketing Spend</span>
                <span className="font-medium">5%</span>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
              <div className="flex items-center space-x-2">
                <AlertCircle className="h-4 w-4 text-yellow-600" />
                <p className="text-xs text-yellow-800">
                  Industry benchmarks for Boston restaurants
                </p>
              </div>
            </div>
          </div>
        </div>
      </SectionCard>
    </div>
  );
};

export default BusinessAnalytics; 