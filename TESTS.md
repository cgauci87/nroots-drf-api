## Table of contents
1. [Unit Testing](#unit-testing)
2. [Validator Testing](#validator-testing)
3. [Manual Testing](#manual-testing)
    1. [URL Testing](#url-testing)
    2. [CRUD Testing](#crud-testing)
    3. [Search, Filter, Sort Functionality Testing](#search-filter-sort-functionality-testing)

***

# Unit Testing
I have performed the following unit tests:

![Unit Tests](https://res.cloudinary.com/dgroams94/image/upload/v1677408230/readme_images/nroots-drf-api/unit_tests_zznilt.png)


Results:

![Unit Tests results](https://res.cloudinary.com/dgroams94/image/upload/v1677408255/readme_images/nroots-drf-api/unit_tests_results_d4vtwu.png)


***

# Validator Testing

All python files passed through the PEP8 validator (pycodestyle) with no issues, apart from some long-line errors which were rectifed. Two long-line error remains in cms/tests.py (line 84 , line 89) due to Cloudinary url: 
![Validator Test results for settings.py](https://res.cloudinary.com/dgroams94/image/upload/v1677410857/readme_images/nroots-drf-api/validator_testing_results_ssnnuv.png)

***

# Manual Testing

## URL testing 
All urls were tested (development and deployed) and all worked as expected. 
![URL testing](https://res.cloudinary.com/dgroams94/image/upload/v1677419021/readme_images/nroots-drf-api/urls_dev_deployed_uqqlrc.png)

## CRUD testing
All apps were tested to ensure appropriate CRUD functionality was present in the development version of DRF.
![CRUD testing](https://res.cloudinary.com/dgroams94/image/upload/v1677419021/readme_images/nroots-drf-api/crud_wtyqsb.png)

## Search, Filter, Sort Functionality Testing
Search, filter and sort were tested, to ensure correct results were returned for Shop and CMS app. 
![Search Filter Sort testing](https://res.cloudinary.com/dgroams94/image/upload/v1677419021/readme_images/nroots-drf-api/search_filter_sort_pullxo.png)
