# Changelog

---

## Version 0.x.x

---
### Version 0.0.1 (2021.05.02)

- Launch project from project ds_zacks

---

### Version 0.0.2 (2021.05.03)

- Update README.md.
  - Add Best Practices.
- Update `preprocessing.standardize`.
  - Now support standardizing specified columns of df by passing argument `columns`.
- Update `regression.linearRegression`.
  - Now support group by data based on labels from a column by passing argument `colorGroupBy`.

---

### Version 0.0.3 (2021.05.06)

- Add module `statisticalTest`
  - Return a proper Statistical Test for users' requirements.
- Add module `simulation`
  - Move all methods from `hypothesisTesting` to `simulation`
  - Add method `chisquare`, which returns a DataFrame object of Chi-Square test.
- Bug fix: `simulation.bootstrapping`
  - Correct the spelling false. Change `bootstraping` to `bootstrapping`
  - Move parameter `repetition` from method `bootstrapping` to class `hypothesisTesting`
- Update: `simulation.histogram`
  - Now support turn off display CI on plot, which controlled by argument `show_CI=False`
- Update: `README.md`
  - Add Dev Version link