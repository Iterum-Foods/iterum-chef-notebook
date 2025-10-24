import React from 'react';
import { useApp } from '../../contexts/AppContext';
import FormField from '../ui/FormField';
import SectionCard from '../ui/SectionCard';

const ManagementTeam = () => {
  const { state, actions } = useApp();
  const data = state.businessPlan.managementTeam;

  const handleFieldChange = (field, value) => {
    actions.updateBusinessPlan('managementTeam', { [field]: value });
  };

  return (
    <div className="animate-fade-in">
      <SectionCard 
        title="Management Team & Organization" 
        description="Outline your management structure and key personnel."
        color="orange"
      >
        <div className="space-y-6">
          <FormField
            label="Key Personnel"
            type="textarea"
            value={data.keyPersonnel}
            onChange={(value) => handleFieldChange('keyPersonnel', value)}
            placeholder="List key team members, their roles, experience, and qualifications"
            rows={4}
          />
          
          <FormField
            label="Organizational Structure"
            type="textarea"
            value={data.organizationalStructure}
            onChange={(value) => handleFieldChange('organizationalStructure', value)}
            placeholder="Describe reporting relationships and organizational hierarchy"
            rows={3}
          />
          
          <FormField
            label="Advisors & Board Members"
            type="textarea"
            value={data.advisors}
            onChange={(value) => handleFieldChange('advisors', value)}
            placeholder="External advisors, board members, mentors, and consultants"
            rows={3}
          />
          
          <FormField
            label="Compensation Plan"
            type="textarea"
            value={data.compensationPlan}
            onChange={(value) => handleFieldChange('compensationPlan', value)}
            placeholder="Salary structures, equity participation, incentive programs"
            rows={3}
          />
        </div>
      </SectionCard>
    </div>
  );
};

export default ManagementTeam; 