import React, { useState } from 'react';
import { useApp } from '../../contexts/AppContext';
import { 
  Plus, 
  Copy, 
  Trash2, 
  Edit3, 
  Clock, 
  FileText, 
  CheckCircle,
  GitCompare,
  ChevronDown,
  X
} from 'lucide-react';

const DraftManager = ({ isOpen, onClose }) => {
  const { state, actions } = useApp();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingDraft, setEditingDraft] = useState(null);
  const [newDraftName, setNewDraftName] = useState('');
  const [selectedForComparison, setSelectedForComparison] = useState([]);

  const currentDraft = state.drafts.find(draft => draft.id === state.currentDraftId);

  const handleCreateDraft = (e) => {
    e.preventDefault();
    if (!newDraftName.trim()) return;

    actions.createDraft(newDraftName.trim());
    setNewDraftName('');
    setShowCreateForm(false);
    actions.showMessage('Success', `New draft "${newDraftName}" created!`, 'success');
  };

  const handleDuplicateDraft = (draftId) => {
    const originalDraft = state.drafts.find(d => d.id === draftId);
    if (!originalDraft) return;

    const duplicateName = `${originalDraft.name} (Copy)`;
    actions.duplicateDraft(draftId, duplicateName);
    actions.showMessage('Success', `Draft duplicated as "${duplicateName}"`, 'success');
  };

  const handleDeleteDraft = (draftId) => {
    const draftToDelete = state.drafts.find(d => d.id === draftId);
    if (!draftToDelete) return;

    if (state.drafts.length === 1) {
      actions.showMessage('Warning', 'Cannot delete the last remaining draft', 'error');
      return;
    }

    const confirmDelete = window.confirm(
      `Are you sure you want to delete "${draftToDelete.name}"? This action cannot be undone.`
    );

    if (confirmDelete) {
      actions.deleteDraft(draftId);
      actions.showMessage('Success', `Draft "${draftToDelete.name}" deleted`, 'success');
    }
  };

  const handleRenameDraft = (draftId, newName) => {
    if (!newName.trim()) return;
    
    actions.updateDraft(draftId, { name: newName.trim() });
    setEditingDraft(null);
    actions.showMessage('Success', 'Draft renamed successfully', 'success');
  };

  const handleSwitchDraft = (draftId) => {
    if (draftId === state.currentDraftId) return;
    
    actions.setCurrentDraftId(draftId);
    const draft = state.drafts.find(d => d.id === draftId);
    actions.showMessage('Info', `Switched to "${draft?.name}"`, 'info');
  };

  const toggleComparisonSelection = (draftId) => {
    setSelectedForComparison(prev => {
      if (prev.includes(draftId)) {
        return prev.filter(id => id !== draftId);
      } else if (prev.length < 2) {
        return [...prev, draftId];
      } else {
        // Replace the first selected if already 2 selected
        return [prev[1], draftId];
      }
    });
  };

  const handleStartComparison = () => {
    if (selectedForComparison.length === 2) {
      actions.setDraftComparison({
        isVisible: true,
        draftIds: selectedForComparison
      });
      setSelectedForComparison([]);
      onClose();
    }
  };

  const formatDate = (date) => {
    if (!date) return 'Unknown';
    const d = date instanceof Date ? date : new Date(date);
    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Draft Manager</h2>
            <p className="text-gray-600 mt-1">
              Manage your business plan drafts - create variations, compare scenarios
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Actions Bar */}
        <div className="p-4 bg-gray-50 border-b border-gray-200">
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => setShowCreateForm(true)}
              className="btn-primary flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>New Draft</span>
            </button>

            {selectedForComparison.length === 2 && (
              <button
                onClick={handleStartComparison}
                className="btn-secondary flex items-center space-x-2"
              >
                <GitCompare className="w-4 h-4" />
                <span>Compare Selected</span>
              </button>
            )}

            <div className="text-sm text-gray-600">
              {selectedForComparison.length > 0 && (
                <span>
                  {selectedForComparison.length}/2 selected for comparison
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Create Draft Form */}
        {showCreateForm && (
          <div className="p-4 bg-blue-50 border-b border-blue-200">
            <form onSubmit={handleCreateDraft} className="flex items-center space-x-3">
              <input
                type="text"
                value={newDraftName}
                onChange={(e) => setNewDraftName(e.target.value)}
                placeholder="Enter draft name (e.g., 'North End Location', 'Fast Casual Concept')"
                className="form-input flex-1"
                autoFocus
              />
              <button type="submit" className="btn-primary">
                Create
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowCreateForm(false);
                  setNewDraftName('');
                }}
                className="btn-secondary"
              >
                Cancel
              </button>
            </form>
          </div>
        )}

        {/* Drafts List */}
        <div className="flex-1 overflow-y-auto max-h-96">
          {state.drafts.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-600">No Drafts Yet</h3>
              <p className="text-gray-500">Create your first business plan draft to get started</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {state.drafts.map((draft) => (
                <div
                  key={draft.id}
                  className={`p-4 hover:bg-gray-50 transition-colors ${
                    draft.id === state.currentDraftId ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 flex-1">
                      {/* Selection Checkbox for Comparison */}
                      <input
                        type="checkbox"
                        checked={selectedForComparison.includes(draft.id)}
                        onChange={() => toggleComparisonSelection(draft.id)}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                      />

                      {/* Draft Info */}
                      <div className="flex-1 cursor-pointer" onClick={() => handleSwitchDraft(draft.id)}>
                        <div className="flex items-center space-x-3">
                          {editingDraft === draft.id ? (
                            <input
                              type="text"
                              defaultValue={draft.name}
                              className="text-lg font-semibold bg-white border rounded px-2 py-1"
                              autoFocus
                              onClick={(e) => e.stopPropagation()}
                              onBlur={(e) => handleRenameDraft(draft.id, e.target.value)}
                              onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                  handleRenameDraft(draft.id, e.target.value);
                                } else if (e.key === 'Escape') {
                                  setEditingDraft(null);
                                }
                              }}
                            />
                          ) : (
                            <h3 className="text-lg font-semibold text-gray-900">{draft.name}</h3>
                          )}
                          
                          {draft.id === state.currentDraftId && (
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              <CheckCircle className="w-3 h-3 mr-1" />
                              Current
                            </span>
                          )}
                        </div>
                        
                        <div className="flex items-center text-sm text-gray-500 mt-1 space-x-4">
                          <div className="flex items-center space-x-1">
                            <Clock className="w-4 h-4" />
                            <span>Updated {formatDate(draft.updatedAt)}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <FileText className="w-4 h-4" />
                            <span>Created {formatDate(draft.createdAt)}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setEditingDraft(draft.id);
                        }}
                        className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                        title="Rename"
                      >
                        <Edit3 className="w-4 h-4" />
                      </button>
                      
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDuplicateDraft(draft.id);
                        }}
                        className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                        title="Duplicate"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                      
                      {state.drafts.length > 1 && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteDraft(draft.id);
                          }}
                          className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-gray-50 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              {state.drafts.length} draft{state.drafts.length !== 1 ? 's' : ''} total
              {currentDraft && (
                <span className="ml-2">
                  • Currently editing: <span className="font-medium">{currentDraft.name}</span>
                </span>
              )}
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="text-xs text-gray-500">
                💡 Tip: Create different drafts for location variations, concept changes, or scenario planning
              </div>
              <button onClick={onClose} className="btn-primary">
                Done
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DraftManager; 