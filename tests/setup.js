// Test setup for Iterum Chef Notebook

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Setup test utilities
global.testUtils = {
  createMockUser: (overrides = {}) => ({
    id: 'test-user-1',
    name: 'Test Chef',
    email: 'test@iterum.com',
    role: 'Chef',
    avatar: '👨‍🍳',
    createdAt: new Date().toISOString(),
    isDefault: false,
    ...overrides
  }),
  
  createMockProject: (overrides = {}) => ({
    id: 'test-project-1',
    name: 'Test Project',
    description: 'A test project',
    is_default: false,
    is_active: true,
    color_theme: '#3B82F6',
    owner_id: 'test-user-1',
    recipe_count: 0,
    menu_count: 0,
    equipment_count: 0,
    ...overrides
  }),
  
  mockFetch: (response, status = 200) => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: status < 400,
        status,
        json: () => Promise.resolve(response),
        text: () => Promise.resolve(JSON.stringify(response))
      })
    );
  }
};

console.log('🧪 Test environment setup complete');
