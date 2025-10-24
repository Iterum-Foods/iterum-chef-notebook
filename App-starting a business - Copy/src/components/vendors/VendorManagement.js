import React, { useState, useMemo } from 'react';
import { useApp } from '../../contexts/AppContext';
import FormField from '../ui/FormField';
import SectionCard from '../ui/SectionCard';
import { Plus, Phone, Mail, Globe, MapPin, Building, Search, Filter } from 'lucide-react';

const VendorManagement = () => {
  const { state, actions } = useApp();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showAddForm, setShowAddForm] = useState(false);

  // Complete Boston restaurant vendor directory (45+ real contacts)
  const initialVendors = [
    // Food Suppliers
    { id: 1, name: "Tedd Rama", company: "Baldor Foods", email: "bbweborders@baldorfoods.com", 
      category: "Food Supplier", description: "Major food distributor serving Boston restaurants", priority: "high" },
    { id: 2, name: "Todd Evens", company: "Sysco Foods", email: "Todd.Evans@sysco.com", phone: "00.669.4440 ext. 8317", 
      mobile: "617-780-9516", fax: "877.655.6443", website: "https://www.sysco.com/", category: "Food Supplier", 
      description: "Leading foodservice distributor with extensive Boston coverage", priority: "high" },
    { id: 3, name: "Joe Sosonoff", company: "Taza Chocolate", email: "jsosnoff@tazachocolate.com", phone: "617 937 9550", 
      website: "tazachcolate.com", category: "Food Supplier", description: "Local Boston chocolate manufacturer", priority: "medium" },
    { id: 4, name: "", company: "Atomic Coffee Roasters", category: "Beverage Supplier", 
      description: "Local coffee roaster for specialty coffee", priority: "medium" },
    { id: 5, name: "Danny Nathan", company: "Cold Craft Juicery", email: "dannynathan@gmail.com", phone: "978-590-3203", 
      category: "Beverage Supplier", description: "Fresh juice and smoothie supplier", priority: "low" },
    { id: 6, name: "Amie Raskin", company: "Intelligentsia Coffee Inc", email: "araskin@intelligentsiacoffee.com", 
      mobile: "917 355 0693", website: "www.intelligentsiacoffee.com", category: "Beverage Supplier", 
      address: "1850 W Fulton St, Chicago, IL 60612", description: "Premium specialty coffee roaster", priority: "medium" },
    { id: 7, name: "", company: "Pain D'avignon", category: "Food Supplier", 
      description: "Artisanal bread and bakery products", priority: "medium" },

    // Equipment & Supplies
    { id: 8, name: "Craig Newton", company: "Supplies on the Fly", email: "cnewton@suppliesonthefly.com", 
      phone: "781.422.2411", mobile: "617-823.0175", fax: "877.417.5311", website: "https://www.suppliesonthefly.com/", 
      category: "Restaurant Supplies", description: "Restaurant equipment and supplies with fast delivery", priority: "high" },
    { id: 9, name: "Jeff Sullivan", company: "Boston Showcase Company", email: "jeff@bostonshowcase.com", 
      phone: "617‐965‐1100", website: "https://www.bostonshowcase.com", category: "Equipment", 
      address: "66 Winchester St. PO Box 610254, Newton Highlands, MA 02461", 
      description: "Restaurant equipment and display cases - local Boston company", priority: "high" },
    { id: 10, name: "Russ", company: "Espresso Plus", email: "service@espressoplus.com", phone: "781-391-2400", 
      category: "Equipment", description: "Espresso machines and coffee equipment", priority: "medium" },
    { id: 11, name: "", company: "Webrestaurant", category: "Restaurant Supplies", 
      description: "Online restaurant supply store", priority: "medium" },
    { id: 12, name: "", company: "Amazon Business", category: "Restaurant Supplies", 
      description: "Business marketplace for supplies and equipment", priority: "low" },
    { id: 13, name: "", company: "Wayfair", category: "Restaurant Supplies", 
      description: "Furniture and decor for restaurant spaces", priority: "low" },
    { id: 14, name: "", company: "Alibaba", category: "Restaurant Supplies", 
      description: "International wholesale marketplace", priority: "low" },

    // Services - Cleaning & Maintenance
    { id: 15, name: "George Clark", company: "Ecolab", email: "george.clark@ecolab.com", phone: "603-417-8594", 
      category: "Cleaning & Sanitation", description: "Commercial cleaning and sanitation solutions", priority: "high" },
    { id: 16, name: "Greg Winn", company: "Metropolitan Linen", email: "gregw@metropolitanlinen.com", 
      phone: "617-839-7419", category: "Linen Service", description: "Commercial linen and uniform services", priority: "high" },
    { id: 17, name: "Danny Najanjo", company: "Waltham Pest Services", email: "DNaranjo@walthamservices.com", 
      phone: "617-620-1936", website: "www.WalthamServices.com", category: "Pest Control", 
      address: "9 Erie Dr, Natick, MA 01760", description: "Commercial pest control services", priority: "high" },
    { id: 18, name: "", company: "Johns Plumbing and Heating", category: "Maintenance", 
      description: "Plumbing and heating services", priority: "medium" },

    // Construction & Engineering
    { id: 19, name: "Ryan Pinkham", company: "Pink Projects", email: "ryan@pinkproj.com", phone: "781-264-2304", 
      website: "https://www.pinkproj.com/", category: "Construction", address: "251 heath St. #508, Jamaica Plain, MA 2130", 
      description: "Restaurant construction and renovation - Jamaica Plain based", priority: "high" },
    { id: 20, name: "Paul Mancini", company: "Trinity Construction", email: "pmancini@trinitybcm.com", 
      phone: "781.305.2733", mobile: "781.983.4477", website: "trinitybuildingusa.com", category: "Construction", 
      description: "Commercial construction and buildouts", priority: "high" },
    { id: 21, name: "Karen Troville", company: "CS Ventilation", email: "Karen@csventilation.com", 
      phone: "781-246-9300", website: "https://csventilation.com/", category: "HVAC", 
      address: "34 Broadway Street Wakefield, Ma, 01880", description: "Commercial kitchen ventilation systems", priority: "high" },
    { id: 22, name: "Donna Hagens", company: "BLW Engineers", email: "dhagens@blwengineers.com", phone: "(978) 486-4301 x10", 
      address: "311 Great Road P.O. Box 1551, Littleton, MA 01460", category: "Engineering", 
      description: "Engineering and design services", priority: "medium" },

    // Security & Technology
    { id: 23, name: "Molly Castor", company: "Frontpoint Security", email: "Molly.Castor@frontpointsecurity.com", 
      phone: "833-408-8428", website: "https://www.frontpointsecurity.com/", category: "Security", 
      description: "Commercial security systems and monitoring", priority: "medium" },
    { id: 24, name: "", company: "Crutchfield", email: "commercialaudio@crutchfield.com", phone: "276-325-6060", 
      website: "www.crutchfield.com", category: "Audio/Visual", description: "Commercial audio and visual systems", priority: "low" },
    { id: 25, name: "RockBot", company: "Rockbot, Inc.", email: "billing@rockbot.com", phone: "415-813-6020", 
      website: "www.rockbot.com", address: "1308 Broadway, Oakland, CA 94612", category: "Audio/Visual", 
      description: "Background music and entertainment systems", priority: "low" },

    // Telecommunications & Internet
    { id: 26, name: "Aaron Senn", company: "Verizon Wireless", email: "aaron.senn@verizonwireless.com", 
      category: "Telecommunications", description: "Business mobile and wireless services", priority: "medium" },
    { id: 27, name: "Angelique Sansoucie", company: "Comcast", email: "Angelique_Sansoucie@comcast.com", phone: "603-695-8450", 
      fax: "866-855-9798", website: "https://business.comcast.com/", category: "Telecommunications", 
      address: "676 Island Pond Road, Manchester, NH, 03109", description: "Business internet and phone services", priority: "medium" },

    // Utilities
    { id: 28, name: "", company: "National Grid", category: "Utilities", 
      description: "Electricity and gas utility provider", priority: "high" },
    { id: 29, name: "", company: "Eversource", category: "Utilities", 
      description: "Electricity utility provider", priority: "high" },

    // POS & Software
    { id: 30, name: "", company: "Toast POS", category: "Software/POS", 
      description: "Restaurant point-of-sale and management system", priority: "high" },
    { id: 31, name: "", company: "Quickbooks", category: "Software/POS", 
      description: "Accounting and financial management software", priority: "high" },
    { id: 32, name: "", company: "Xtrachef", category: "Software/POS", 
      description: "Restaurant invoice and cost management platform", priority: "medium" },

    // Marketing & Branding
    { id: 33, name: "", company: "Squarespace", website: "Squarespace.com", category: "Marketing/Branding", 
      address: "New York, NY 10014", description: "Website building and hosting platform", priority: "medium" },
    { id: 34, name: "Custom ink", company: "Custom Ink", email: "service@customink.com", phone: "800-293-4232", 
      website: "customink.com", category: "Marketing/Branding", description: "Custom apparel and promotional products", priority: "low" },
    { id: 35, name: "Printful", company: "Printful", email: "support@info.printful.com", website: "printful.com", 
      category: "Marketing/Branding", description: "Print-on-demand and fulfillment services", priority: "low" },

    // Professional Services
    { id: 36, name: "Steve Dillberg", company: "Schofer Dillberg & Company, Inc.", email: "steve@sdc-cpa.com", 
      phone: "(508) 545-8403", website: "https://www.sdc-cpa.com/", address: "MA", category: "Accounting/Finance", 
      description: "Certified public accounting services", priority: "high" },
    { id: 37, name: "Michael Grimmer", company: "Vestwell", email: "michael.grimmer@vestwell.com", 
      category: "Accounting/Finance", description: "401(k) and retirement plan services", priority: "low" },
    { id: 38, name: "Josh Duttweiller", company: "Josh Duttweiller", email: "joshua.duttweiler@me.com", phone: "(585)735-5082", 
      website: "https://joshuaduttweiler.com/", category: "Consulting", description: "Business consulting services", priority: "low" },

    // Apparel & Uniforms
    { id: 39, name: "Michelle Smith", company: "Tilit", email: "Michelle@tilitnyc.com", phone: "646-422-7197", 
      website: "https://www.tilitnyc.com/", address: "64 Allen St. #2, New York, NY 10002", category: "Uniforms", 
      description: "Chef and restaurant uniforms", priority: "medium" },
    { id: 40, name: "Jessica Dubrowskij", company: "Blue Drop", email: "Jessica@bluedrop.com", phone: "877-662-7873", 
      category: "Uniforms", description: "Custom uniforms and workwear", priority: "low" },

    // Specialty Services
    { id: 41, name: "", company: "Instacart", category: "Delivery/Logistics", 
      description: "Grocery delivery and shopping service", priority: "low" },
    { id: 42, name: "", company: "Clippership Wharf Family LLC", category: "Real Estate", 
      description: "Commercial real estate services", priority: "medium" },
    { id: 43, name: "", company: "yourbrandcafe", address: "24 Norfolk Ave, South Easton, MA 2375", category: "Food Supplier", 
      description: "Specialty coffee and cafe products", priority: "low" }
  ];

  const vendors = state.vendors.length > 0 ? state.vendors : initialVendors;

  const categories = [
    'Food Supplier', 'Beverage Supplier', 'Restaurant Supplies', 'Equipment', 
    'Cleaning & Sanitation', 'Linen Service', 'HVAC', 'Security', 'Pest Control', 
    'Construction', 'Engineering', 'Telecommunications', 'Utilities', 'Software/POS',
    'Marketing/Branding', 'Accounting/Finance', 'Consulting', 'Uniforms', 
    'Audio/Visual', 'Maintenance', 'Delivery/Logistics', 'Real Estate', 'Other'
  ];

  // Filter vendors based on search and category
  const filteredVendors = useMemo(() => {
    return vendors.filter(vendor => {
      const matchesSearch = vendor.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          vendor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          vendor.category.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = selectedCategory === 'all' || vendor.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }, [vendors, searchTerm, selectedCategory]);

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleAddVendor = (vendorData) => {
    const newVendor = {
      ...vendorData,
      id: Date.now(),
      priority: vendorData.priority || 'medium'
    };
    actions.addVendor(newVendor);
    setShowAddForm(false);
  };

  const handleRemoveVendor = (vendorId) => {
    if (window.confirm('Are you sure you want to remove this vendor?')) {
      actions.removeVendor(vendorId);
    }
  };

  return (
    <div className="animate-fade-in space-y-6">
      {/* Header Section */}
      <SectionCard 
        title="Boston Restaurant Vendor Directory" 
        description="Manage your supplier relationships with pre-loaded Boston-area vendors and local industry contacts."
        color="yellow"
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-yellow-100 p-4 rounded-lg">
            <h4 className="font-semibold text-yellow-800 mb-2">Total Vendors</h4>
            <div className="text-2xl font-bold text-yellow-700">{vendors.length}</div>
          </div>
          <div className="bg-orange-100 p-4 rounded-lg">
            <h4 className="font-semibold text-orange-800 mb-2">High Priority</h4>
            <div className="text-2xl font-bold text-orange-700">
              {vendors.filter(v => v.priority === 'high').length}
            </div>
          </div>
          <div className="bg-green-100 p-4 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">Categories</h4>
            <div className="text-2xl font-bold text-green-700">
              {new Set(vendors.map(v => v.category)).size}
            </div>
          </div>
        </div>

        {/* Search and Filter Controls */}
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search vendors by name, company, or category..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="form-input pl-10"
            />
          </div>
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="form-input pl-10 pr-8"
            >
              <option value="all">All Categories</option>
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Add Vendor</span>
          </button>
        </div>
      </SectionCard>

      {/* Vendor Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredVendors.map((vendor) => (
          <div key={vendor.id} className="card hover-lift">
            <div className="flex justify-between items-start mb-3">
              <h3 className="font-bold text-lg text-gray-900">{vendor.company}</h3>
              <div className="flex items-center space-x-2">
                <span className={`text-xs px-2 py-1 rounded-full ${getPriorityColor(vendor.priority)}`}>
                  {vendor.priority}
                </span>
                <button
                  onClick={() => handleRemoveVendor(vendor.id)}
                  className="text-red-500 hover:text-red-700 text-sm"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="space-y-2 mb-4">
              <div className="flex items-center space-x-2">
                <Building className="w-4 h-4 text-gray-500" />
                <span className="text-sm font-medium text-gray-700">{vendor.name}</span>
              </div>
              
              <div className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full inline-block">
                {vendor.category}
              </div>

              {vendor.description && (
                <p className="text-sm text-gray-600 mt-2">{vendor.description}</p>
              )}
            </div>

            <div className="space-y-2 text-sm">
              {vendor.email && (
                <div className="flex items-center space-x-2">
                  <Mail className="w-4 h-4 text-gray-400" />
                  <a href={`mailto:${vendor.email}`} className="text-blue-600 hover:underline">
                    {vendor.email}
                  </a>
                </div>
              )}
              
              {vendor.phone && (
                <div className="flex items-center space-x-2">
                  <Phone className="w-4 h-4 text-gray-400" />
                  <a href={`tel:${vendor.phone}`} className="text-blue-600 hover:underline">
                    {vendor.phone}
                  </a>
                </div>
              )}
              
              {vendor.website && (
                <div className="flex items-center space-x-2">
                  <Globe className="w-4 h-4 text-gray-400" />
                  <a href={vendor.website} target="_blank" rel="noopener noreferrer" 
                     className="text-blue-600 hover:underline">
                    Visit Website
                  </a>
                </div>
              )}
              
              {vendor.address && (
                <div className="flex items-center space-x-2">
                  <MapPin className="w-4 h-4 text-gray-400" />
                  <span className="text-gray-600">{vendor.address}</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {filteredVendors.length === 0 && (
        <div className="text-center py-12">
          <h3 className="text-lg font-semibold text-gray-600 mb-2">No vendors found</h3>
          <p className="text-gray-500">Try adjusting your search terms or filter criteria.</p>
        </div>
      )}

      {/* Add Vendor Modal */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold text-gray-900">Add New Vendor</h3>
                <button
                  onClick={() => setShowAddForm(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              
              <VendorForm 
                onSubmit={handleAddVendor}
                onCancel={() => setShowAddForm(false)}
                categories={categories}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Vendor Form Component
const VendorForm = ({ onSubmit, onCancel, categories }) => {
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    email: '',
    phone: '',
    mobile: '',
    website: '',
    address: '',
    category: 'Other',
    description: '',
    priority: 'medium'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.name || !formData.company) {
      alert('Name and Company are required fields.');
      return;
    }
    onSubmit(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <FormField
          label="Contact Name"
          type="text"
          value={formData.name}
          onChange={(value) => handleChange('name', value)}
          placeholder="John Smith"
          required
        />
        <FormField
          label="Company Name"
          type="text"
          value={formData.company}
          onChange={(value) => handleChange('company', value)}
          placeholder="ABC Restaurant Supply"
          required
        />
        <FormField
          label="Email"
          type="email"
          value={formData.email}
          onChange={(value) => handleChange('email', value)}
          placeholder="contact@company.com"
        />
        <FormField
          label="Phone"
          type="text"
          value={formData.phone}
          onChange={(value) => handleChange('phone', value)}
          placeholder="617-555-0123"
        />
        <FormField
          label="Mobile"
          type="text"
          value={formData.mobile}
          onChange={(value) => handleChange('mobile', value)}
          placeholder="617-555-0124"
        />
        <FormField
          label="Website"
          type="url"
          value={formData.website}
          onChange={(value) => handleChange('website', value)}
          placeholder="https://company.com"
        />
        <FormField
          label="Category"
          type="select"
          value={formData.category}
          onChange={(value) => handleChange('category', value)}
          options={categories.map(cat => ({ value: cat, label: cat }))}
        />
        <FormField
          label="Priority"
          type="select"
          value={formData.priority}
          onChange={(value) => handleChange('priority', value)}
          options={[
            { value: 'high', label: 'High Priority' },
            { value: 'medium', label: 'Medium Priority' },
            { value: 'low', label: 'Low Priority' }
          ]}
        />
      </div>
      
      <FormField
        label="Address"
        type="text"
        value={formData.address}
        onChange={(value) => handleChange('address', value)}
        placeholder="123 Main St, Boston, MA 02101"
      />
      
      <FormField
        label="Description"
        type="textarea"
        value={formData.description}
        onChange={(value) => handleChange('description', value)}
        placeholder="Brief description of services or products..."
        rows={3}
      />

      <div className="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="btn-secondary"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="btn-primary"
        >
          Add Vendor
        </button>
      </div>
    </form>
  );
};

export default VendorManagement; 