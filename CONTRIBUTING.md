
# Contributing to Seed to Shelf Contracts

## Contract Change Discipline

### Versioning Rules
- **MAJOR** version (X.0.0): Breaking changes to existing APIs
- **MINOR** version (0.X.0): Backward-compatible new functionality  
- **PATCH** version (0.0.X): Backward-compatible bug fixes

### Change Process
1. **Proposal**: Create an issue describing the contract change
2. **Review**: Get approval from at least 2 maintainers
3. **Implementation**: Make changes in the contracts package
4. **Testing**: Verify both TypeScript and Python builds work
5. **Version Bump**: Update version in both package.json and setup.py
6. **Release**: Create GitHub release to trigger automated publishing

### Breaking Changes
Breaking changes require:
- 30-day deprecation notice for consumers
- Migration guide for affected services
- Coordination with all dependent teams

### Schema Validation
All contract changes must:
- Pass TypeScript compilation
- Pass Python package build
- Include appropriate test cases
- Maintain backward compatibility within major version

### Dependencies
- **chefgrid** should pin to specific major versions: `^0.1.0`
- Services should regularly update to latest patch versions
- Major version updates require coordinated deployment

### Testing
- Run `npm test` in contracts directory
- Verify Python package builds with `python setup.py check`
- Test integration with sample data in both languages
