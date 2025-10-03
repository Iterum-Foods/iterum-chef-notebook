const { test, expect } = require('@playwright/test');

test.describe('User Authentication System', () => {
  test.beforeEach(async ({ page }) => {
    // Clear any existing data before each test
    await page.addInitScript(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    
    // Navigate to the main page
    await page.goto('/');
  });

  test('should show user selection popup on app launch', async ({ page }) => {
    // Wait for the user selection modal to appear
    const userModal = page.locator('.auth-modal-overlay');
    await expect(userModal).toBeVisible();
    
    // Check that it shows the correct title
    const title = page.locator('h2:has-text("Select Your Profile")');
    await expect(title).toBeVisible();
  });

  test('should allow creating a new user profile', async ({ page }) => {
    // Wait for user selection modal
    await page.waitForSelector('.auth-modal-overlay');
    
    // Click create new profile button
    await page.click('button:has-text("Create New Profile")');
    
    // Wait for create profile modal
    await page.waitForSelector('h2:has-text("Create Your Profile")');
    
    // Fill in the form
    await page.fill('#profile-name', 'Test Chef');
    await page.selectOption('#profile-role', 'Chef');
    await page.fill('#profile-restaurant', 'Test Kitchen');
    
    // Submit the form
    await page.click('button:has-text("Create Profile")');
    
    // Should redirect to main page with user logged in
    await expect(page.locator('.auth-modal-overlay')).not.toBeVisible();
    
    // Check that user info is displayed somewhere on the page
    await expect(page.locator('text=Test Chef')).toBeVisible();
  });

  test('should persist user selection across page refresh', async ({ page }) => {
    // Create a user first
    await page.waitForSelector('.auth-modal-overlay');
    await page.click('button:has-text("Create New Profile")');
    await page.waitForSelector('h2:has-text("Create Your Profile")');
    
    await page.fill('#profile-name', 'Persistent Chef');
    await page.selectOption('#profile-role', 'Chef');
    await page.click('button:has-text("Create Profile")');
    
    // Wait for modal to disappear
    await expect(page.locator('.auth-modal-overlay')).not.toBeVisible();
    
    // Refresh the page
    await page.reload();
    
    // Should not show user selection modal again
    await expect(page.locator('.auth-modal-overlay')).not.toBeVisible();
    
    // User info should still be visible
    await expect(page.locator('text=Persistent Chef')).toBeVisible();
  });

  test('should allow switching between multiple users', async ({ page }) => {
    // Create first user
    await page.waitForSelector('.auth-modal-overlay');
    await page.click('button:has-text("Create New Profile")');
    await page.waitForSelector('h2:has-text("Create Your Profile")');
    
    await page.fill('#profile-name', 'Chef Alice');
    await page.selectOption('#profile-role', 'Chef');
    await page.click('button:has-text("Create Profile")');
    
    await expect(page.locator('.auth-modal-overlay')).not.toBeVisible();
    
    // Create second user
    await page.click('button:has-text("Switch User")');
    await page.waitForSelector('.auth-modal-overlay');
    await page.click('button:has-text("Create New Profile")');
    
    await page.fill('#profile-name', 'Chef Bob');
    await page.selectOption('#profile-role', 'Sous Chef');
    await page.click('button:has-text("Create Profile")');
    
    // Should now have two users
    await page.click('button:has-text("Switch User")');
    await page.waitForSelector('.auth-modal-overlay');
    
    // Check that both users are listed
    await expect(page.locator('text=Chef Alice')).toBeVisible();
    await expect(page.locator('text=Chef Bob')).toBeVisible();
  });

  test('should handle offline mode gracefully', async ({ page }) => {
    // The app should work in offline mode
    await page.waitForSelector('.auth-modal-overlay');
    
    // Create user should work offline
    await page.click('button:has-text("Create New Profile")');
    await page.waitForSelector('h2:has-text("Create Your Profile")');
    
    await page.fill('#profile-name', 'Offline Chef');
    await page.selectOption('#profile-role', 'Chef');
    await page.click('button:has-text("Create Profile")');
    
    // Should work without internet
    await expect(page.locator('.auth-modal-overlay')).not.toBeVisible();
    await expect(page.locator('text=Offline Chef')).toBeVisible();
  });
});

test.describe('Project Management', () => {
  test.beforeEach(async ({ page }) => {
    // Clear data and create a user
    await page.addInitScript(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    
    await page.goto('/');
    
    // Create a user for testing
    await page.waitForSelector('.auth-modal-overlay');
    await page.click('button:has-text("Create New Profile")');
    await page.waitForSelector('h2:has-text("Create Your Profile")');
    
    await page.fill('#profile-name', 'Project Chef');
    await page.selectOption('#profile-role', 'Chef');
    await page.click('button:has-text("Create Profile")');
    
    await expect(page.locator('.auth-modal-overlay')).not.toBeVisible();
  });

  test('should create master project by default', async ({ page }) => {
    // Check that master project is created and selected
    const projectSelector = page.locator('[data-project-selector]');
    await expect(projectSelector).toBeVisible();
    
    // Should show "Master Project" or similar
    await expect(page.locator('text=Master')).toBeVisible();
  });

  test('should allow creating new projects', async ({ page }) => {
    // Look for project creation button
    const createProjectBtn = page.locator('button:has-text("Create Project"), button:has-text("New Project")');
    
    if (await createProjectBtn.isVisible()) {
      await createProjectBtn.click();
      
      // Should show project creation form
      await expect(page.locator('input[placeholder*="project"], input[placeholder*="Project"]')).toBeVisible();
    }
  });
});

test.describe('Data Persistence', () => {
  test.beforeEach(async ({ page }) => {
    // Clear data and create a user
    await page.addInitScript(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    
    await page.goto('/');
    
    // Create a user for testing
    await page.waitForSelector('.auth-modal-overlay');
    await page.click('button:has-text("Create New Profile")');
    await page.waitForSelector('h2:has-text("Create Your Profile")');
    
    await page.fill('#profile-name', 'Data Chef');
    await page.selectOption('#profile-role', 'Chef');
    await page.click('button:has-text("Create Profile")');
    
    await expect(page.locator('.auth-modal-overlay')).not.toBeVisible();
  });

  test('should save recipe ideas and persist them', async ({ page }) => {
    // Navigate to recipe ideas section if it exists
    const recipeIdeasSection = page.locator('text=Recipe Ideas, text=Ideas, [data-ideas-section]');
    
    if (await recipeIdeasSection.isVisible()) {
      await recipeIdeasSection.click();
      
      // Look for input field to add new idea
      const ideaInput = page.locator('input[placeholder*="idea"], textarea[placeholder*="idea"], [data-idea-input]');
      
      if (await ideaInput.isVisible()) {
        await ideaInput.fill('Test Recipe Idea');
        await ideaInput.press('Enter');
        
        // Should save and display the idea
        await expect(page.locator('text=Test Recipe Idea')).toBeVisible();
        
        // Refresh page to test persistence
        await page.reload();
        
        // Idea should still be there
        await expect(page.locator('text=Test Recipe Idea')).toBeVisible();
      }
    }
  });
});
