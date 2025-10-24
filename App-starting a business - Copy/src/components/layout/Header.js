import React, { useState } from 'react';
import { useApp } from '../../contexts/AppContext';
import { Building2, Save, User, FileText, ChevronDown, GitCompare } from 'lucide-react';
import DraftManager from './DraftManager';
import DraftComparison from './DraftComparison';

const Header = () => {
  const { state, actions } = useApp();
  const [showDraftManager, setShowDraftManager] = useState(false);
  const [showDraftDropdown, setShowDraftDropdown] = useState(false);

  const currentDraft = state.drafts.find(draft => draft.id === state.currentDraftId);

  const handleSave = async () => {
    await actions.saveData();
  };

  const handleSwitchDraft = (draftId) => {
    actions.setCurrentDraftId(draftId);
    setShowDraftDropdown(false);
  };

  const handleCreateQuickDraft = () => {
    const draftName = `Draft ${state.drafts.length + 1}`;
    actions.createDraft(draftName);
    setShowDraftDropdown(false);
  };

  return (
    <>
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-3">
                <Building2 className="w-8 h-8 text-blue-600" />
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    Boston Restaurant Business Planning
                  </h1>
                  <p className="text-sm text-gray-600">
                    Create comprehensive restaurant business plans with local market data
                  </p>
                </div>
              </div>

              {/* Draft Selector */}
              {currentDraft && (
                <div className="relative">
                  <button
                    onClick={() => setShowDraftDropdown(!showDraftDropdown)}
                    className="flex items-center space-x-2 px-4 py-2 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
                  >
                    <FileText className="w-4 h-4 text-blue-600" />
                    <div className="text-left">
                      <div className="text-sm font-semibold text-blue-900">
                        {currentDraft.name}
                      </div>
                      <div className="text-xs text-blue-600">
                        Current Draft
                      </div>
                    </div>
                    <ChevronDown className="w-4 h-4 text-blue-600" />
                  </button>

                  {/* Draft Dropdown */}
                  {showDraftDropdown && (
                    <div className="absolute top-full left-0 mt-2 w-80 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                      <div className="p-3 border-b border-gray-200">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900">Your Drafts</h3>
                          <button
                            onClick={() => {
                              setShowDraftManager(true);
                              setShowDraftDropdown(false);
                            }}
                            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                          >
                            Manage All
                          </button>
                        </div>
                      </div>
                      <div className="max-h-64 overflow-y-auto">
                        {state.drafts.map((draft) => (
                          <button
                            key={draft.id}
                            onClick={() => handleSwitchDraft(draft.id)}
                            className={`w-full text-left px-3 py-2 hover:bg-gray-50 transition-colors ${
                              draft.id === state.currentDraftId ? 'bg-blue-50' : ''
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <div className="flex-1">
                                <div className="font-medium text-gray-900">{draft.name}</div>
                                <div className="text-xs text-gray-500">
                                  Updated {new Date(draft.updatedAt).toLocaleDateString()}
                                </div>
                              </div>
                              {draft.id === state.currentDraftId && (
                                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                              )}
                            </div>
                          </button>
                        ))}
                      </div>
                      <div className="p-3 border-t border-gray-200 space-y-2">
                        <button
                          onClick={handleCreateQuickDraft}
                          className="w-full btn-primary text-sm py-2"
                        >
                          + Create New Draft
                        </button>
                        {state.drafts.length >= 2 && (
                          <button
                            onClick={() => {
                              setShowDraftManager(true);
                              setShowDraftDropdown(false);
                            }}
                            className="w-full btn-secondary text-sm py-2 flex items-center justify-center space-x-2"
                          >
                            <GitCompare className="w-4 h-4" />
                            <span>Compare Drafts</span>
                          </button>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>
                  {state.isAuthenticated ? `User: ${state.userId?.slice(-8)}` : 'Anonymous User'}
                </span>
              </div>

              {/* Draft Count Badge */}
              {state.drafts.length > 1 && (
                <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-600">
                  <FileText className="w-4 h-4" />
                  <span>{state.drafts.length} drafts</span>
                </div>
              )}
              
              <button
                onClick={handleSave}
                disabled={state.isLoading || !state.currentDraftId}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                <span className="hidden sm:inline">Save Draft</span>
                <span className="sm:hidden">Save</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Draft Manager Modal */}
      <DraftManager 
        isOpen={showDraftManager} 
        onClose={() => setShowDraftManager(false)} 
      />

      {/* Draft Comparison Modal */}
      <DraftComparison />

      {/* Click outside handler for dropdown */}
      {showDraftDropdown && (
        <div 
          className="fixed inset-0 z-40" 
          onClick={() => setShowDraftDropdown(false)}
        />
      )}
    </>
  );
};

export default Header; 