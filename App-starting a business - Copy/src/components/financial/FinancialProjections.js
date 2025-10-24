import React, { useMemo } from 'react';
import { useApp } from '../../contexts/AppContext';
import FormField from '../ui/FormField';
import SectionCard from '../ui/SectionCard';
import { Calculator, TrendingUp, DollarSign, AlertTriangle } from 'lucide-react';

const FinancialProjections = () => {
  const { state, actions } = useApp();
  const data = state.financialData;

  const handleFieldChange = (section, field, value) => {
    const numValue = value === '' ? 0 : parseFloat(value) || 0;
    actions.updateFinancialData(section, { [field]: numValue });
  };

  // Boston Restaurant Industry Benchmarks
  const bostonBenchmarks = {
    avgRentPerSqFt: 45, // $45/sq ft annually in Boston
    avgUtilitiesPerSqFt: 8, // $8/sq ft annually
    avgSeatPrice: 40, // Average check per person
    avgTurnovers: 2.5, // Table turnovers per day
    avgFoodCostPercent: 0.28, // 28% food costs
    avgLaborPercent: 0.32, // 32% labor costs
    avgRevPerSeat: 75000, // Annual revenue per seat
  };

  // Calculate key metrics
  const calculations = useMemo(() => {
    const totalRevenue = data.revenue.foodSales + data.revenue.beverageSales + 
                        data.revenue.merchandiseSales + data.revenue.cateringSales + 
                        data.revenue.otherRevenue;

    const totalCogs = (data.revenue.foodSales * data.cogs.foodCogsPercent) +
                     (data.revenue.beverageSales * data.cogs.beverageCogsPercent) +
                     (data.revenue.merchandiseSales * data.cogs.merchandiseCogsPercent) +
                     (data.revenue.cateringSales * data.cogs.cateringCogsPercent) +
                     (data.revenue.otherRevenue * data.cogs.otherCogsPercent);

    const grossProfit = totalRevenue - totalCogs;
    const grossMargin = totalRevenue > 0 ? (grossProfit / totalRevenue) * 100 : 0;

    const totalOpEx = data.operatingExpenses.rent + data.operatingExpenses.utilities +
                     data.operatingExpenses.insurance + data.operatingExpenses.marketing +
                     data.operatingExpenses.legalAccounting + data.operatingExpenses.repairsMaintenance +
                     data.operatingExpenses.supplies + data.operatingExpenses.adminOffice +
                     data.operatingExpenses.otherOperatingExpenses;

    const totalPayroll = (data.operatingExpenses.salaryOwners + data.operatingExpenses.salaryFullTime +
                         data.operatingExpenses.salaryPartTime) * (1 + data.operatingExpenses.payrollTaxRate);

    const totalExpenses = totalOpEx + totalPayroll;
    const netIncome = grossProfit - totalExpenses;
    const netMargin = totalRevenue > 0 ? (netIncome / totalRevenue) * 100 : 0;

    const totalStartupCosts = data.startupCosts.leaseholdImprovements + data.startupCosts.kitchenEquipment +
                             data.startupCosts.furnitureFixtures + data.startupCosts.initialInventory +
                             data.startupCosts.preOpeningSalaries + data.startupCosts.depositsLicenses +
                             data.startupCosts.initialMarketing + data.startupCosts.contingency;

    const totalFunding = data.fundingSources.ownersEquity + data.fundingSources.investorFunds +
                        data.fundingSources.bankLoans + data.fundingSources.otherFunding;

    const breakEvenRevenue = totalExpenses / (grossMargin / 100);

    return {
      totalRevenue,
      totalCogs,
      grossProfit,
      grossMargin,
      totalOpEx,
      totalPayroll,
      totalExpenses,
      netIncome,
      netMargin,
      totalStartupCosts,
      totalFunding,
      breakEvenRevenue,
      fundingGap: totalStartupCosts - totalFunding
    };
  }, [data]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getHealthStatus = (actual, benchmark, higher = false) => {
    const ratio = actual / benchmark;
    if (higher) {
      return ratio >= 1.1 ? 'excellent' : ratio >= 0.9 ? 'good' : 'needs-attention';
    } else {
      return ratio <= 0.9 ? 'excellent' : ratio <= 1.1 ? 'good' : 'needs-attention';
    }
  };

  return (
    <div className="animate-fade-in space-y-8">
      {/* Header with Boston Context */}
      <SectionCard 
        title="Boston Restaurant Financial Projections" 
        description="Comprehensive financial modeling tailored for Boston's restaurant market with local benchmarks and regulations."
        color="blue"
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-blue-100 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">Boston Market Context</h4>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Avg rent: ${bostonBenchmarks.avgRentPerSqFt}/sq ft/year</li>
              <li>• Target food cost: {(bostonBenchmarks.avgFoodCostPercent * 100).toFixed(0)}%</li>
              <li>• Target labor: {(bostonBenchmarks.avgLaborPercent * 100).toFixed(0)}%</li>
            </ul>
          </div>
          <div className="bg-green-100 p-4 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">Revenue Targets</h4>
            <ul className="text-sm text-green-700 space-y-1">
              <li>• Avg check: ${bostonBenchmarks.avgSeatPrice}</li>
              <li>• Table turns: {bostonBenchmarks.avgTurnovers}/day</li>
              <li>• Revenue/seat: ${(bostonBenchmarks.avgRevPerSeat / 1000).toFixed(0)}k/year</li>
            </ul>
          </div>
          <div className="bg-purple-100 p-4 rounded-lg">
            <h4 className="font-semibold text-purple-800 mb-2">Your Performance</h4>
            <ul className="text-sm text-purple-700 space-y-1">
              <li>• Gross margin: {calculations.grossMargin.toFixed(1)}%</li>
              <li>• Net margin: {calculations.netMargin.toFixed(1)}%</li>
              <li>• Break-even: {formatCurrency(calculations.breakEvenRevenue)}</li>
            </ul>
          </div>
        </div>
      </SectionCard>

      {/* Revenue Projections */}
      <SectionCard title="Revenue Projections (Year 1)" color="green">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            label="Food Sales (Annual)"
            type="number"
            value={data.revenue.foodSales}
            onChange={(value) => handleFieldChange('revenue', 'foodSales', value)}
            placeholder="500000"
          />
          <FormField
            label="Beverage Sales (Annual)"
            type="number"
            value={data.revenue.beverageSales}
            onChange={(value) => handleFieldChange('revenue', 'beverageSales', value)}
            placeholder="150000"
          />
          <FormField
            label="Catering Sales (Annual)"
            type="number"
            value={data.revenue.cateringSales}
            onChange={(value) => handleFieldChange('revenue', 'cateringSales', value)}
            placeholder="25000"
          />
          <FormField
            label="Other Revenue (Annual)"
            type="number"
            value={data.revenue.otherRevenue}
            onChange={(value) => handleFieldChange('revenue', 'otherRevenue', value)}
            placeholder="10000"
          />
        </div>
        <div className="mt-6 p-4 bg-green-50 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-lg font-semibold">Total Annual Revenue:</span>
            <span className="text-2xl font-bold text-green-600">
              {formatCurrency(calculations.totalRevenue)}
            </span>
          </div>
        </div>
      </SectionCard>

      {/* Cost of Goods Sold */}
      <SectionCard title="Cost of Goods Sold (COGS)" color="orange">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            label="Food COGS % (Boston avg: 28%)"
            type="number"
            value={data.cogs.foodCogsPercent}
            onChange={(value) => handleFieldChange('cogs', 'foodCogsPercent', value / 100)}
            placeholder="28"
            step="0.1"
          />
          <FormField
            label="Beverage COGS % (Target: 20-25%)"
            type="number"
            value={data.cogs.beverageCogsPercent * 100}
            onChange={(value) => handleFieldChange('cogs', 'beverageCogsPercent', value / 100)}
            placeholder="22"
            step="0.1"
          />
          <FormField
            label="Catering COGS % (Target: 30-35%)"
            type="number"
            value={data.cogs.cateringCogsPercent * 100}
            onChange={(value) => handleFieldChange('cogs', 'cateringCogsPercent', value / 100)}
            placeholder="32"
            step="0.1"
          />
          <FormField
            label="Other COGS % (Target: 10-15%)"
            type="number"
            value={data.cogs.otherCogsPercent * 100}
            onChange={(value) => handleFieldChange('cogs', 'otherCogsPercent', value / 100)}
            placeholder="12"
            step="0.1"
          />
        </div>
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-orange-50 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="font-semibold">Total COGS:</span>
              <span className="text-xl font-bold text-orange-600">
                {formatCurrency(calculations.totalCogs)}
              </span>
            </div>
          </div>
          <div className="p-4 bg-green-50 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="font-semibold">Gross Profit:</span>
              <span className="text-xl font-bold text-green-600">
                {formatCurrency(calculations.grossProfit)}
              </span>
            </div>
          </div>
        </div>
      </SectionCard>

      {/* Operating Expenses */}
      <SectionCard title="Boston Operating Expenses (Annual)" color="red">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            label="Rent (Boston avg: $45/sq ft)"
            type="number"
            value={data.operatingExpenses.rent}
            onChange={(value) => handleFieldChange('operatingExpenses', 'rent', value)}
            placeholder="120000"
          />
          <FormField
            label="Utilities (Boston avg: $8/sq ft)"
            type="number"
            value={data.operatingExpenses.utilities}
            onChange={(value) => handleFieldChange('operatingExpenses', 'utilities', value)}
            placeholder="18000"
          />
          <FormField
            label="Insurance (Required in MA)"
            type="number"
            value={data.operatingExpenses.insurance}
            onChange={(value) => handleFieldChange('operatingExpenses', 'insurance', value)}
            placeholder="15000"
          />
          <FormField
            label="Marketing & Advertising"
            type="number"
            value={data.operatingExpenses.marketing}
            onChange={(value) => handleFieldChange('operatingExpenses', 'marketing', value)}
            placeholder="25000"
          />
          <FormField
            label="Legal & Accounting"
            type="number"
            value={data.operatingExpenses.legalAccounting}
            onChange={(value) => handleFieldChange('operatingExpenses', 'legalAccounting', value)}
            placeholder="8000"
          />
          <FormField
            label="Repairs & Maintenance"
            type="number"
            value={data.operatingExpenses.repairsMaintenance}
            onChange={(value) => handleFieldChange('operatingExpenses', 'repairsMaintenance', value)}
            placeholder="12000"
          />
        </div>

        <h3 className="text-lg font-semibold mt-8 mb-4">Boston Payroll (MA min wage: $15/hr)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            label="Owner/Manager Salary"
            type="number"
            value={data.operatingExpenses.salaryOwners}
            onChange={(value) => handleFieldChange('operatingExpenses', 'salaryOwners', value)}
            placeholder="75000"
          />
          <FormField
            label="Full-Time Staff (Annual)"
            type="number"
            value={data.operatingExpenses.salaryFullTime}
            onChange={(value) => handleFieldChange('operatingExpenses', 'salaryFullTime', value)}
            placeholder="180000"
          />
          <FormField
            label="Part-Time Staff (Annual)"
            type="number"
            value={data.operatingExpenses.salaryPartTime}
            onChange={(value) => handleFieldChange('operatingExpenses', 'salaryPartTime', value)}
            placeholder="120000"
          />
          <FormField
            label="Payroll Tax Rate (MA: ~12%)"
            type="number"
            value={data.operatingExpenses.payrollTaxRate * 100}
            onChange={(value) => handleFieldChange('operatingExpenses', 'payrollTaxRate', value / 100)}
            placeholder="12"
            step="0.1"
          />
        </div>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-red-50 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="font-semibold">Operating Expenses:</span>
              <span className="text-lg font-bold text-red-600">
                {formatCurrency(calculations.totalOpEx)}
              </span>
            </div>
          </div>
          <div className="p-4 bg-purple-50 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="font-semibold">Total Payroll:</span>
              <span className="text-lg font-bold text-purple-600">
                {formatCurrency(calculations.totalPayroll)}
              </span>
            </div>
          </div>
          <div className="p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="font-semibold">Net Income:</span>
              <span className={`text-lg font-bold ${calculations.netIncome >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(calculations.netIncome)}
              </span>
            </div>
          </div>
        </div>
      </SectionCard>

      {/* Boston Startup Costs */}
      <SectionCard title="Boston Restaurant Startup Costs" color="purple">
        <div className="mb-4 p-4 bg-purple-50 rounded-lg">
          <h4 className="font-semibold text-purple-800 mb-2">Boston-Specific Requirements:</h4>
          <ul className="text-sm text-purple-700 space-y-1">
            <li>• Boston business license & food service permit</li>
            <li>• MA alcoholic beverage license (if applicable)</li>
            <li>• Fire department approval & sprinkler system</li>
            <li>• Board of Health inspection & certification</li>
          </ul>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            label="Leasehold Improvements"
            type="number"
            value={data.startupCosts.leaseholdImprovements}
            onChange={(value) => handleFieldChange('startupCosts', 'leaseholdImprovements', value)}
            placeholder="200000"
          />
          <FormField
            label="Kitchen Equipment"
            type="number"
            value={data.startupCosts.kitchenEquipment}
            onChange={(value) => handleFieldChange('startupCosts', 'kitchenEquipment', value)}
            placeholder="125000"
          />
          <FormField
            label="Furniture & Fixtures"
            type="number"
            value={data.startupCosts.furnitureFixtures}
            onChange={(value) => handleFieldChange('startupCosts', 'furnitureFixtures', value)}
            placeholder="40000"
          />
          <FormField
            label="Initial Inventory"
            type="number"
            value={data.startupCosts.initialInventory}
            onChange={(value) => handleFieldChange('startupCosts', 'initialInventory', value)}
            placeholder="15000"
          />
          <FormField
            label="Boston Permits & Licenses"
            type="number"
            value={data.startupCosts.depositsLicenses}
            onChange={(value) => handleFieldChange('startupCosts', 'depositsLicenses', value)}
            placeholder="25000"
          />
          <FormField
            label="Pre-Opening Marketing"
            type="number"
            value={data.startupCosts.initialMarketing}
            onChange={(value) => handleFieldChange('startupCosts', 'initialMarketing', value)}
            placeholder="15000"
          />
        </div>

        <div className="mt-6 p-4 bg-purple-100 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-lg font-semibold">Total Startup Investment:</span>
            <span className="text-2xl font-bold text-purple-600">
              {formatCurrency(calculations.totalStartupCosts)}
            </span>
          </div>
        </div>
      </SectionCard>

      {/* Financial Health Dashboard */}
      <SectionCard title="Financial Health Dashboard" color="gray">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className={`p-4 rounded-lg ${calculations.grossMargin >= 65 ? 'bg-green-100' : calculations.grossMargin >= 60 ? 'bg-yellow-100' : 'bg-red-100'}`}>
            <div className="flex items-center space-x-2 mb-2">
              <TrendingUp className="w-5 h-5" />
              <span className="font-semibold">Gross Margin</span>
            </div>
            <div className="text-2xl font-bold">{calculations.grossMargin.toFixed(1)}%</div>
            <div className="text-sm text-gray-600">Target: 65%+</div>
          </div>

          <div className={`p-4 rounded-lg ${calculations.netMargin >= 10 ? 'bg-green-100' : calculations.netMargin >= 5 ? 'bg-yellow-100' : 'bg-red-100'}`}>
            <div className="flex items-center space-x-2 mb-2">
              <DollarSign className="w-5 h-5" />
              <span className="font-semibold">Net Margin</span>
            </div>
            <div className="text-2xl font-bold">{calculations.netMargin.toFixed(1)}%</div>
            <div className="text-sm text-gray-600">Target: 10%+</div>
          </div>

          <div className={`p-4 rounded-lg ${calculations.fundingGap <= 0 ? 'bg-green-100' : 'bg-red-100'}`}>
            <div className="flex items-center space-x-2 mb-2">
              <Calculator className="w-5 h-5" />
              <span className="font-semibold">Funding Gap</span>
            </div>
            <div className="text-2xl font-bold">{formatCurrency(Math.abs(calculations.fundingGap))}</div>
            <div className="text-sm text-gray-600">
              {calculations.fundingGap <= 0 ? 'Fully Funded' : 'Additional Needed'}
            </div>
          </div>

          <div className="p-4 bg-blue-100 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <AlertTriangle className="w-5 h-5" />
              <span className="font-semibold">Break-Even</span>
            </div>
            <div className="text-2xl font-bold">{formatCurrency(calculations.breakEvenRevenue)}</div>
            <div className="text-sm text-gray-600">Monthly Revenue Needed</div>
          </div>
        </div>
      </SectionCard>
    </div>
  );
};

export default FinancialProjections; 