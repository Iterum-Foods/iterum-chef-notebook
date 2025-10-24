import React, { useState, useMemo } from 'react';
import SectionCard from '../ui/SectionCard';
import { 
  Package, ChefHat, Coffee, Refrigerator, Zap, 
  CheckCircle, Utensils, Armchair, Music, Shield, Printer, Wifi
} from 'lucide-react';

const EquipmentPlanning = () => {
  const [activeCategory, setActiveCategory] = useState('kitchen');
  const [selectedItems, setSelectedItems] = useState(new Set());

  // Kitchen Equipment (Back of House)
  const kitchenEquipment = [
    {
      id: 'commercial-range',
      name: 'Commercial Gas Range',
      category: 'Cooking',
      icon: ChefHat,
      essential: true,
      estimatedCost: 3500,
      description: '6-burner commercial range with oven',
      specifications: '36" wide, BTU 180,000',
      vendors: ['Boston Showcase Company', 'Supplies on the Fly'],
      maintenance: 'Annual cleaning and calibration',
      energyType: 'Gas'
    },
    {
      id: 'deep-fryer',
      name: 'Commercial Deep Fryer',
      category: 'Cooking',
      icon: ChefHat,
      essential: true,
      estimatedCost: 2200,
      description: 'Dual-basket deep fryer',
      specifications: '40-50 lb oil capacity',
      vendors: ['Boston Showcase Company'],
      maintenance: 'Daily oil filtering, weekly deep clean',
      energyType: 'Gas/Electric'
    },
    {
      id: 'commercial-grill',
      name: 'Commercial Flat Top Grill',
      category: 'Cooking',
      icon: ChefHat,
      essential: false,
      estimatedCost: 2800,
      description: 'Flat top grill for burgers and sandwiches',
      specifications: '36" wide, temperature range 200-550°F',
      vendors: ['Boston Showcase Company'],
      maintenance: 'Daily seasoning, weekly deep clean',
      energyType: 'Gas'
    },
    {
      id: 'walk-in-cooler',
      name: 'Walk-in Cooler',
      category: 'Refrigeration',
      icon: Refrigerator,
      essential: true,
      estimatedCost: 8500,
      description: 'Walk-in refrigeration unit',
      specifications: '8x8x8 ft, 35-38°F',
      vendors: ['Boston Showcase Company'],
      maintenance: 'Monthly coil cleaning, annual service',
      energyType: 'Electric'
    },
    {
      id: 'reach-in-freezer',
      name: 'Reach-in Freezer',
      category: 'Refrigeration',
      icon: Refrigerator,
      essential: true,
      estimatedCost: 3200,
      description: '2-door commercial freezer',
      specifications: '54" wide, 0-10°F',
      vendors: ['Boston Showcase Company', 'Supplies on the Fly'],
      maintenance: 'Monthly defrost, quarterly service',
      energyType: 'Electric'
    },
    {
      id: 'prep-tables',
      name: 'Stainless Steel Prep Tables',
      category: 'Prep',
      icon: Utensils,
      essential: true,
      estimatedCost: 800,
      description: 'Set of 3 prep tables with storage',
      specifications: '30" x 72" each, with undershelf',
      vendors: ['Boston Showcase Company', 'Supplies on the Fly'],
      maintenance: 'Daily sanitizing',
      energyType: 'None'
    },
    {
      id: 'commercial-dishwasher',
      name: 'Commercial Dishwasher',
      category: 'Cleaning',
      icon: Package,
      essential: true,
      estimatedCost: 4500,
      description: 'High-temp door-type dishwasher',
      specifications: '24" rack size, 180°F sanitizing',
      vendors: ['Boston Showcase Company'],
      maintenance: 'Daily cleaning, monthly descaling',
      energyType: 'Electric + Water'
    },
    {
      id: 'hood-system',
      name: 'Kitchen Ventilation Hood',
      category: 'Ventilation',
      icon: Zap,
      essential: true,
      estimatedCost: 7500,
      description: 'Commercial kitchen exhaust hood with fire suppression',
      specifications: '12 ft hood with Type K suppression',
      vendors: ['CS Ventilation'],
      maintenance: 'Quarterly cleaning, annual inspection',
      energyType: 'Electric'
    },
    {
      id: 'espresso-machine',
      name: 'Commercial Espresso Machine',
      category: 'Beverage',
      icon: Coffee,
      essential: false,
      estimatedCost: 5500,
      description: '2-group espresso machine',
      specifications: 'Semi-automatic, steam wand',
      vendors: ['Espresso Plus', 'Intelligentsia Coffee'],
      maintenance: 'Daily cleaning, weekly descaling',
      energyType: 'Electric + Water'
    }
  ];

  // Front of House Equipment
  const frontOfHouseEquipment = [
    {
      id: 'pos-system',
      name: 'Point of Sale System',
      category: 'Technology',
      icon: Printer,
      essential: true,
      estimatedCost: 2500,
      description: 'Complete POS system with terminals',
      specifications: '2 terminals, payment processing',
      vendors: ['Toast POS'],
      maintenance: 'Software updates, annual service',
      energyType: 'Electric + Internet'
    },
    {
      id: 'dining-tables',
      name: 'Dining Tables',
      category: 'Furniture',
      icon: Armchair,
      essential: true,
      estimatedCost: 3000,
      description: 'Restaurant dining tables (set of 12)',
      specifications: '30" x 30" and 24" x 42" tops',
      vendors: ['Boston Showcase Company', 'Wayfair'],
      maintenance: 'Daily cleaning, annual refinishing',
      energyType: 'None'
    },
    {
      id: 'dining-chairs',
      name: 'Dining Chairs',
      category: 'Furniture',
      icon: Armchair,
      essential: true,
      estimatedCost: 2400,
      description: 'Restaurant chairs (set of 48)',
      specifications: 'Commercial-grade, stackable',
      vendors: ['Boston Showcase Company', 'Wayfair'],
      maintenance: 'Weekly inspection, annual reupholstering',
      energyType: 'None'
    },
    {
      id: 'sound-system',
      name: 'Sound System',
      category: 'Audio/Visual',
      icon: Music,
      essential: false,
      estimatedCost: 1800,
      description: 'Background music and announcement system',
      specifications: 'Wireless, multi-zone control',
      vendors: ['Crutchfield', 'Rockbot'],
      maintenance: 'Annual inspection',
      energyType: 'Electric'
    },
    {
      id: 'security-system',
      name: 'Security System',
      category: 'Security',
      icon: Shield,
      essential: true,
      estimatedCost: 2200,
      description: 'Cameras and alarm system',
      specifications: '8 cameras, 24/7 monitoring',
      vendors: ['Frontpoint Security'],
      maintenance: 'Monthly testing, annual service',
      energyType: 'Electric + Internet'
    },
    {
      id: 'internet-phone',
      name: 'Internet & Phone System',
      category: 'Technology',
      icon: Wifi,
      essential: true,
      estimatedCost: 800,
      description: 'Business internet and phone setup',
      specifications: 'High-speed internet, VoIP phones',
      vendors: ['Comcast', 'Verizon Wireless'],
      maintenance: 'Annual contract renewal',
      energyType: 'Electric'
    }
  ];

  // Small Equipment & Supplies
  const smallEquipment = [
    { id: 'knives', name: 'Professional Knife Set', cost: 500, essential: true },
    { id: 'cutting-boards', name: 'Commercial Cutting Boards', cost: 200, essential: true },
    { id: 'pots-pans', name: 'Commercial Cookware Set', cost: 800, essential: true },
    { id: 'serving-plates', name: 'Dinnerware Set (100 place settings)', cost: 600, essential: true },
    { id: 'glassware', name: 'Glassware Set', cost: 400, essential: true },
    { id: 'utensils', name: 'Flatware Set', cost: 300, essential: true },
    { id: 'cleaning-supplies', name: 'Initial Cleaning Supplies', cost: 350, essential: true },
    { id: 'uniforms', name: 'Staff Uniforms (Initial Set)', cost: 800, essential: true },
    { id: 'first-aid', name: 'First Aid Station', cost: 150, essential: true },
    { id: 'office-supplies', name: 'Office Supplies', cost: 200, essential: false }
  ];

  // Opening Day Checklist
  const openingChecklist = [
    { category: 'Kitchen Setup', items: [
      'All cooking equipment tested and calibrated',
      'Refrigeration units at proper temperatures',
      'Fire suppression system tested',
      'Ventilation system operational',
      'All small wares organized and accessible',
      'Initial food inventory stocked',
      'Cleaning supplies fully stocked'
    ]},
    { category: 'Front of House Setup', items: [
      'POS system configured and tested',
      'All furniture arranged per floor plan',
      'Sound system tested',
      'Security system armed and tested',
      'Internet and phone systems operational',
      'Emergency lighting tested',
      'All signage installed and lit'
    ]},
    { category: 'Safety & Compliance', items: [
      'Fire extinguishers checked and accessible',
      'First aid kit stocked and accessible',
      'Safety data sheets organized',
      'Emergency procedures posted',
      'Maximum occupancy signs posted',
      'Handwashing stations stocked',
      'All permits and licenses displayed'
    ]},
    { category: 'Staff Preparation', items: [
      'All equipment operation training completed',
      'POS system training completed',
      'Safety procedures training completed',
      'Menu and preparation training completed',
      'Service standards training completed',
      'Emergency procedures reviewed',
      'Uniforms distributed and fitted'
    ]}
  ];

  const allEquipment = [...kitchenEquipment, ...frontOfHouseEquipment];

  // Calculate costs
  const calculations = useMemo(() => {
    const selectedEquipment = allEquipment.filter(item => selectedItems.has(item.id));
    const essentialEquipment = allEquipment.filter(item => item.essential);
    const smallEquipmentCost = smallEquipment
      .filter(item => item.essential)
      .reduce((sum, item) => sum + item.cost, 0);

    return {
      selectedTotal: selectedEquipment.reduce((sum, item) => sum + item.estimatedCost, 0),
      essentialTotal: essentialEquipment.reduce((sum, item) => sum + item.estimatedCost, 0),
      smallEquipmentTotal: smallEquipmentCost,
      grandTotal: essentialEquipment.reduce((sum, item) => sum + item.estimatedCost, 0) + smallEquipmentCost
    };
  }, [selectedItems, allEquipment, smallEquipment]);

  const categories = [
    { id: 'kitchen', name: 'Kitchen Equipment', icon: ChefHat, equipment: kitchenEquipment },
    { id: 'front-house', name: 'Front of House', icon: Armchair, equipment: frontOfHouseEquipment },
    { id: 'small-equipment', name: 'Small Equipment', icon: Package, equipment: smallEquipment },
    { id: 'checklist', name: 'Opening Checklist', icon: CheckCircle, equipment: [] }
  ];

  const toggleSelection = (itemId) => {
    const newSelection = new Set(selectedItems);
    if (newSelection.has(itemId)) {
      newSelection.delete(itemId);
    } else {
      newSelection.add(itemId);
    }
    setSelectedItems(newSelection);
  };

  const selectAllEssential = () => {
    const essentialIds = allEquipment.filter(item => item.essential).map(item => item.id);
    setSelectedItems(new Set(essentialIds));
  };

  const formatCurrency = (amount) => new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(amount);

  const renderEquipmentCard = (equipment) => (
    <div 
      key={equipment.id}
      className={`border rounded-lg p-4 cursor-pointer transition-all ${
        selectedItems.has(equipment.id) 
          ? 'border-blue-500 bg-blue-50' 
          : 'border-gray-200 hover:border-gray-300'
      }`}
      onClick={() => toggleSelection(equipment.id)}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <equipment.icon className="h-6 w-6 text-gray-600 mt-1" />
          <div className="flex-1">
            <div className="flex items-center space-x-2">
              <h4 className="font-semibold text-gray-900">{equipment.name}</h4>
              {equipment.essential && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                  Essential
                </span>
              )}
            </div>
            <p className="text-sm text-gray-600 mt-1">{equipment.description}</p>
            {equipment.specifications && (
              <p className="text-xs text-gray-500 mt-1">{equipment.specifications}</p>
            )}
            <div className="flex items-center space-x-4 mt-2">
              <span className="text-lg font-bold text-green-600">
                {formatCurrency(equipment.estimatedCost)}
              </span>
              <span className="text-xs text-gray-500">{equipment.energyType}</span>
            </div>
            <div className="mt-2">
              <p className="text-xs text-gray-600">
                <strong>Vendors:</strong> {equipment.vendors?.join(', ') || 'Various'}
              </p>
              <p className="text-xs text-gray-600">
                <strong>Maintenance:</strong> {equipment.maintenance}
              </p>
            </div>
          </div>
        </div>
        <div className="ml-4">
          {selectedItems.has(equipment.id) ? (
            <CheckCircle className="h-6 w-6 text-blue-600" />
          ) : (
            <div className="h-6 w-6 border-2 border-gray-300 rounded-full" />
          )}
        </div>
      </div>
    </div>
  );

  const renderSmallEquipment = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {smallEquipment.map(item => (
        <div key={item.id} className="border border-gray-200 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">{item.name}</h4>
              <span className="text-sm font-semibold text-green-600">
                {formatCurrency(item.cost)}
              </span>
            </div>
            {item.essential && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                Essential
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  );

  const renderChecklist = () => (
    <div className="space-y-6">
      {openingChecklist.map((section, index) => (
        <div key={index} className="border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
            {section.category}
          </h4>
          <div className="space-y-2">
            {section.items.map((item, itemIndex) => (
              <label key={itemIndex} className="flex items-center space-x-3 cursor-pointer">
                <input type="checkbox" className="rounded border-gray-300" />
                <span className="text-sm text-gray-700">{item}</span>
              </label>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div className="animate-fade-in space-y-6">
      {/* Header */}
      <SectionCard 
        title="Restaurant Equipment Planning" 
        description="Comprehensive equipment planning and cost estimation for your Boston restaurant"
        color="purple"
      >
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-purple-100 p-4 rounded-lg">
            <h4 className="font-semibold text-purple-800 mb-2">Essential Equipment</h4>
            <div className="text-2xl font-bold text-purple-700">
              {formatCurrency(calculations.essentialTotal)}
            </div>
          </div>
          <div className="bg-blue-100 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">Small Equipment</h4>
            <div className="text-2xl font-bold text-blue-700">
              {formatCurrency(calculations.smallEquipmentTotal)}
            </div>
          </div>
          <div className="bg-green-100 p-4 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">Total Investment</h4>
            <div className="text-2xl font-bold text-green-700">
              {formatCurrency(calculations.grandTotal)}
            </div>
          </div>
          <div className="bg-orange-100 p-4 rounded-lg">
            <h4 className="font-semibold text-orange-800 mb-2">Selected Items</h4>
            <div className="text-2xl font-bold text-orange-700">
              {selectedItems.size}
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-4 mb-6">
          <button
            onClick={selectAllEssential}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
          >
            Select All Essential
          </button>
          <button
            onClick={() => setSelectedItems(new Set())}
            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
          >
            Clear Selection
          </button>
        </div>
      </SectionCard>

      {/* Category Navigation */}
      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setActiveCategory(category.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
                activeCategory === category.id
                  ? 'bg-white text-purple-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <category.icon className="h-5 w-5" />
              <span className="font-medium">{category.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        {activeCategory === 'kitchen' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Kitchen Equipment (Back of House)</h3>
            {kitchenEquipment.map(renderEquipmentCard)}
          </div>
        )}

        {activeCategory === 'front-house' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Front of House Equipment</h3>
            {frontOfHouseEquipment.map(renderEquipmentCard)}
          </div>
        )}

        {activeCategory === 'small-equipment' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Small Equipment & Supplies</h3>
            {renderSmallEquipment()}
          </div>
        )}

        {activeCategory === 'checklist' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Restaurant Opening Day Checklist</h3>
            {renderChecklist()}
          </div>
        )}
      </div>

      {/* Selected Items Summary */}
      {selectedItems.size > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">Selected Equipment Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {allEquipment
              .filter(item => selectedItems.has(item.id))
              .map(item => (
                <div key={item.id} className="bg-white border border-blue-200 rounded-lg p-3">
                  <h4 className="font-medium text-gray-900">{item.name}</h4>
                  <span className="text-sm font-semibold text-green-600">
                    {formatCurrency(item.estimatedCost)}
                  </span>
                </div>
              ))
            }
          </div>
          <div className="mt-4 pt-4 border-t border-blue-200">
            <div className="text-xl font-bold text-blue-900">
              Total Selected: {formatCurrency(calculations.selectedTotal)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EquipmentPlanning; 