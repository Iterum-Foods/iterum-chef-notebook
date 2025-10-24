import React from 'react';
import { useApp } from '../../contexts/AppContext';
import FormField from '../ui/FormField';
import SectionCard from '../ui/SectionCard';

const MarketingStrategy = () => {
  const { state, actions } = useApp();
  const data = state.businessPlan.marketingStrategy;

  const handleFieldChange = (field, value) => {
    actions.updateBusinessPlan('marketingStrategy', { [field]: value });
  };

  return (
    <div className="animate-fade-in">
      <SectionCard 
        title="Marketing & Sales Strategy" 
        description="Outline how you'll attract and retain customers."
        color="pink"
      >
        <div className="space-y-6">
          <FormField
            label="Marketing Mix (4 P's)"
            type="textarea"
            value={data.marketingMix}
            onChange={(value) => handleFieldChange('marketingMix', value)}
            placeholder="Product, Price, Place, Promotion strategy"
            rows={4}
          />
          
          <FormField
            label="Sales Strategy"
            type="textarea"
            value={data.salesStrategy}
            onChange={(value) => handleFieldChange('salesStrategy', value)}
            placeholder="Sales process, channels, team structure, targets"
            rows={3}
          />
          
          <FormField
            label="Customer Acquisition"
            type="textarea"
            value={data.customerAcquisition}
            onChange={(value) => handleFieldChange('customerAcquisition', value)}
            placeholder="How will you find and attract new customers?"
            rows={3}
          />
          
          <FormField
            label="Branding Strategy"
            type="textarea"
            value={data.brandingStrategy}
            onChange={(value) => handleFieldChange('brandingStrategy', value)}
            placeholder="Brand positioning, messaging, visual identity"
            rows={3}
          />
          
          <FormField
            label="Digital Marketing"
            type="textarea"
            value={data.digitalMarketing}
            onChange={(value) => handleFieldChange('digitalMarketing', value)}
            placeholder="Website, social media, SEO, online advertising strategy"
            rows={3}
          />
        </div>
      </SectionCard>
    </div>
  );
};

export default MarketingStrategy; 