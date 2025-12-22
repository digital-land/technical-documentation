---
title: Frontend Build Best Practices
---

This document outlines best practices for frontend build processes in Digital Land projects, based on the approach used in config-manager.

## Architecture

### Build Tool Organization

Use **nps (npm-package-scripts)** to organize build scripts in JavaScript files rather than cluttering package.json:

```javascript
// package-scripts.js
module.exports = {
  scripts: {
    build: {
      stylesheets: 'sass src/scss:output/stylesheets',
      javascripts: 'rollup -c',
    },
    copy: {
      assets: 'copyfiles ...',
      all: 'nps copy.assets copy.images'
    }
  }
};
```

**Benefits:**
- Better organization for complex build processes
- JavaScript logic for conditional builds
- Easier to extend and override base configurations
- Comments and documentation inline with scripts

### Tool Selection

**SASS/SCSS for stylesheets:**
- Industry standard for CSS preprocessing
- Compatible with GOV.UK Frontend
- Variables, mixins, and imports for maintainable styles

**Rollup for JavaScript bundling:**
- Lightweight and focused
- Tree-shaking for smaller bundles
- Simple configuration
- Good for library-style code (vs application frameworks)

**copyfiles for asset management:**
- Cross-platform file copying
- Glob pattern support
- Path manipulation with `-u` flag (strip path segments)
- Handles nested directory structures reliably

## Project Structure

### Source vs Output

Keep clear separation between source and generated files:

```
src/
  scss/           # Source SCSS files
  javascripts/    # Source JS files

application/static/   # Generated files (git-ignored)
  stylesheets/        # Compiled CSS
  javascripts/        # Bundled JS
  images/             # Copied images
  govuk/              # GOV.UK Frontend assets
```

**Rules:**
- Never commit generated files
- Git-ignore entire `application/static/` directory
- Source files in `src/`, output in `application/static/`
- Make it obvious which is which

### Configuration Files

**package.json:**
- Keep scripts simple and readable
- Delegate to nps for complex builds
```json
{
  "scripts": {
    "build": "nps build.stylesheets build.javascripts",
    "watch": "npm-run-all --parallel watch:*"
  }
}
```

**package-scripts.js:**
- Extend shared base scripts
- Override only what's necessary
- Document why overrides exist
```javascript
// Override govukAssets to fix v5 compatibility
govukAssets: 'npx copyfiles -u 4 "node_modules/govuk-frontend/dist/govuk/assets/**" application/static/govuk/'
```

**Project-specific config file:**
```json
// digital-land-frontend.config.json
{
  "scssPath": "./src/scss",
  "jsOutputPath": "application/static/javascripts",
  "stylesheetsOutputPath": "application/static/stylesheets"
}
```

## Shared Build Scripts

**Important:** All Digital Land projects must use `@planning-data/digital-land-frontend` as the single source of shared build scripts. Do not create additional shared build modules - consolidate all shared functionality in digital-land-frontend.

### Contributing to digital-land-frontend

When adding or updating shared build scripts in @planning-data/digital-land-frontend:

**Do:**
- Export nps scripts that projects can extend
- Make paths configurable via config file
- Provide sensible defaults
- Document breaking changes in GOV.UK Frontend versions
- Keep dependencies up to date
- Test changes across multiple consuming projects
- Coordinate updates with team

**Don't:**
- Hardcode paths that assume specific project structure
- Make assumptions about framework (Flask, Django, Express)
- Include framework-specific code
- Make breaking changes without migration guide

### Using digital-land-frontend in Projects

When consuming digital-land-frontend build scripts in a project:

**Do:**
- Extend, don't replace the base scripts
- Override only what's necessary for your project
- Document why overrides exist
- Keep the shared package version in sync across projects
- Test after updating shared package versions

**Don't:**
- Duplicate scripts from the shared package
- Fork the shared package for small changes
- Skip postinstall hooks that run builds

Example override pattern:
```javascript
const dlFrontendScripts = require('@planning-data/digital-land-frontend/package-scripts.js');

module.exports = {
  scripts: {
    ...dlFrontendScripts.scripts,
    copy: {
      ...dlFrontendScripts.scripts.copy,
      // Project-specific override with explanation
      govukAssets: '...'
    }
  }
};
```

## Build Process Order

Build tasks must run in the correct order for the build to succeed:

### Standard Build Sequence

```
1. Copy assets
2. Build stylesheets (SCSS → CSS)
3. Build javascripts (bundle custom JS)
```

**Why this order matters:**

1. **Copy first:** Vendor assets (GOV.UK Frontend, fonts, images) must be in place before compilation
2. **Stylesheets second:** SCSS may reference copied assets (fonts, images) via `url()` paths
3. **JavaScript last:** JS bundles may import stylesheets or reference copied assets

### Implementation

In package.json:
```json
{
  "scripts": {
    "copy": "nps copy.all",
    "build:css": "nps build.stylesheets",
    "build:js": "nps build.javascripts",
    "build": "npm run copy && npm run build:css && npm run build:js"
  },
  "postinstall": "npm run build"
}
```

**Key points:**
- Use `&&` to run sequentially (not `&` which runs in parallel)
- Each step depends on the previous completing successfully
- Postinstall hook ensures fresh checkouts are built automatically

### Watch Mode Exception

During development, watch tasks can run in parallel since initial build is already complete:

```json
{
  "watch:assets": "nps watch.assets",
  "watch:css": "nps watch.stylesheets",
  "watch:js": "nps watch.javascripts",
  "watch": "npm-run-all --parallel watch:*"
}
```

The initial `npm install` runs the sequential build, then watch mode monitors for changes.

## Build Process Integration

### Development Workflow

Provide watch commands for rapid development:

```json
{
  "watch:assets": "nps watch.assets",
  "watch:pages": "flask run --reload",
  "watch": "npm-run-all --parallel watch:*"
}
```

Run both frontend build watching and backend server in parallel.

### Production Workflow

Use postinstall hooks to ensure assets are built:

```json
{
  "postinstall": "npm run copy && npm run build"
}
```

This ensures `npm install` always generates required assets.

### Clean Targets

Provide clean commands to reset to fresh state:

```makefile
clean:
    rm -rf node_modules
    rm -rf application/static/
```

Don't delete and recreate Python venvs during clean (slows developer workflow).

## GOV.UK Frontend Integration

### Version Compatibility

**GOV.UK Frontend v4+ breaking change:**
- v3 and earlier: Assets at `node_modules/govuk-frontend/govuk/assets/`
- v4+: Assets at `node_modules/govuk-frontend/dist/govuk/assets/`

When copying assets, adjust path stripping accordingly:
- v3: `copyfiles -u 2` strips `node_modules/govuk-frontend`
- v5: `copyfiles -u 4` strips `node_modules/govuk-frontend/dist/govuk`

**Document this in your package-scripts.js comments.**

### Asset Organization

SCSS expects govuk assets at specific paths:
```scss
// SCSS imports expect:
@font-face {
  src: url("/static/govuk/assets/fonts/...");
}
```

Ensure your copy scripts put files where SCSS expects them.

### JavaScript Bundles

GOV.UK Frontend v5 provides pre-bundled JavaScript:
```bash
cp node_modules/govuk-frontend/dist/govuk/all.bundle.js application/static/javascripts/govuk/
```

No need to bundle it yourself with Rollup.

## Vendor Assets

### Third-Party Libraries

For libraries not in npm (or old versions):
- Keep in `src/javascripts/vendor/` or `src/css/vendor/`
- Copy to static directory during build
- Document source and version in comments

For modern npm packages:
- Install via npm
- Copy dist files during build
```javascript
copy: {
  accessibleAutocomplete: 'cp node_modules/accessible-autocomplete/dist/* application/static/javascripts/'
}
```

### Ministry of Justice Components

MoJ frontend components should be:
- Installed via npm if available
- Copied to vendor directory
- Version tracked in package.json

## Common Pitfalls

### Path Issues

**Problem:** Assets copied to wrong location, SCSS can't find them.

**Solution:**
- Check SCSS import paths
- Verify copyfiles `-u` flag strips correct number of segments
- Test that files end up where templates/SCSS expect

### Duplicate Dependencies

**Problem:** Multiple versions of digital-land-frontend or duplicate packages.

**Solution:**
- Use consistent package names across repos
- Pin versions in package.json
- Regular audits: `npm ls digital-land-frontend`

### Missing Assets After Updates

**Problem:** New GOV.UK Frontend version, assets in different location.

**Solution:**
- Check GOV.UK Frontend release notes for breaking changes
- Update copyfiles commands
- Test thoroughly after version bumps
- Document version-specific quirks

### Build Not Running

**Problem:** Fresh checkout, assets missing.

**Solution:**
- Ensure postinstall hook runs build
- Document build requirements in README
- Provide `make init` that runs npm install

## Documentation Requirements

Every project using frontend builds should document:

1. **What tools are used** (SASS, Rollup, etc.)
2. **Common commands** (build, watch, copy)
3. **Where generated files go**
4. **That generated files are git-ignored**
5. **Any project-specific customizations**
6. **How to add new JS/CSS files**

Example README section: [config-manager/README.md](https://github.com/digital-land/config-manager#frontend-build)

## Future Considerations

### Vite Migration

Modern alternative to current multi-tool setup:

**Benefits:**
- Single tool replaces SASS + Rollup + copyfiles
- Hot Module Replacement (HMR) for instant feedback
- Faster builds
- Better developer experience

**Trade-offs:**
- Migration effort
- Team learning curve
- Additional configuration for Flask integration

**When to consider:**
- Starting new projects
- Major refactoring of existing projects
- Team wants modern DX improvements

Current setup (nps + SASS + Rollup) is production-ready and well-understood across Digital Land projects. Vite is an optimization, not a requirement.

## Version Control

### What to Commit

**Do commit:**
- Source files (`src/`)
- Build configuration (`package-scripts.js`, `rollup.config.js`)
- Package manifests (`package.json`, `package-lock.json`)
- Build tool configs (`.sassrc`, etc.)

**Don't commit:**
- Generated files (`application/static/`)
- Node modules (`node_modules/`)
- Build artifacts
- Temporary files

### .gitignore

```
# Generated static assets
application/static/

# Dependencies
node_modules/
```

Be aggressive - ignore entire directories, not individual files within them.

## Summary

**Key principles:**
1. **Separate source from generated files**
2. **Use shared scripts with project-specific overrides**
3. **Document why overrides exist**
4. **Automate builds with postinstall hooks**
5. **Keep it simple - don't over-engineer**
6. **Test after dependency updates**
7. **Git-ignore all generated files**

The goal is a build process that:
- Works reliably across environments
- Is easy for new developers to understand
- Requires minimal manual intervention
- Stays consistent across Digital Land projects
