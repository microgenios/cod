#!/usr/bin/env python
# coding: utf-8

# # CS-109: Fall 2015  -- Lab 4
# 
# # Regression in Python
# 
# ***
# This is a very quick run-through of some basic statistical concepts
# 
# * Regression Models
#     * Linear, Logistic
# * Prediction using linear regression
# * Some re-sampling methods    
#     * Train-Test splits
#     * Cross Validation
# 
# Linear regression is used to model and predict continuous outcomes while logistic regression is used to model binary outcomes. We'll see some examples of linear regression as well as Train-test splits.
# 
# 
# The packages we'll cover are: `statsmodels`, `seaborn`, and `scikit-learn`.
# ***

# <img width=600 height=300 src="https://imgs.xkcd.com/comics/sustainable.png"/>
# ***

# In[ ]:


# special IPython command to prepare the notebook for matplotlib
get_ipython().magic(u'matplotlib inline')

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
import statsmodels.api as sm

import seaborn as sns
sns.set_style("whitegrid")
sns.set_context("poster")

# special matplotlib argument for improved plots
from matplotlib import rcParams


# # Part 0: Piazza Posting Guidelines
# ***
# <div class="span5 alert alert-info">
# The high volume of posts on piazza has made it very difficult for us to answer all of your questions.  For this reason, we are taking measures to decrease the volume of posts, and increase their quality.  Below is the general format that we now require for all posts.  ONLY posts that are in this format will be answered by staff.  Posts that are not in this format will be made private, and students will be asked to reformat their question.
# </div>
#  
# 1. At the top of your post, make a list of all the keywords you entered in your piazza search when looking for answers to your question.  Also include a list of keywords you searched in google.  Provide links to all the posts that you read that were relevant, but did not quite answer your question. 
#  
# 2. If you are sure that your question is not a duplicate question, write down your question in as much detail as possible without posting code.  You can post your error messages, and unit tests.
#  
# 3. Include the steps you have taken for debugging, and what the outcome was.  You must have spent at least 30 minutes trying to debug before you post a question. 
#  
# 4. Post your question in the most specific folder possible, for example hw1-1.1 (see @564)
#  
# 5. Follow up!  Describe the solution that worked for you.  Also, click the "resolve" button if your problem has been resolved.
#  
# See @310 for general posting guidelines and etiquette.  

# ***
# # Part 1: Linear Regression
# ### Purpose of linear regression
# ***
# <div class="span5 alert alert-info">
# 
# <p> Given a dataset $X$ and $Y$, linear regression can be used to: </p>
# <ul>
#   <li> Build a <b>predictive model</b> to predict future values of $X_i$ without a $Y$ value.  </li>
#   <li> Model the <b>strength of the relationship</b> between each dependent variable $X_i$ and $Y$</li>
#     <ul>
#       <li> Sometimes not all $X_i$ will have a relationship with $Y$</li>
#       <li> Need to figure out which $X_i$ contributes most information to determine $Y$ </li>
#     </ul>
#    <li>Linear regression is used in so many applications that I won't warrant this with examples. It is in many cases, the first pass prediction algorithm for continuous outcomes. </li>
# </ul>
# </div>
# 
# ### A brief recap
# ***
# 
# [Linear Regression](http://en.wikipedia.org/wiki/Linear_regression) is a method to model the relationship between a set of independent variables $X$ (also knowns as explanatory variables, features, predictors) and a dependent variable $Y$.  This method assumes the relationship between each predictor $X$ is linearly related to the dependent variable $Y$.  
# 
# $$ Y = \beta_0 + \beta_1 X + \epsilon$$
# 
# where $\epsilon$ is considered as an unobservable random variable that adds noise to the linear relationship. This is the simplest form of linear regression (one variable), we'll call this the simple model. 
# 
# * $\beta_0$ is the intercept of the linear model
# 
# * Multiple linear regression is when you have more than one independent variable
#     * $X_1$, $X_2$, $X_3$, $\ldots$
# 
# $$ Y = \beta_0 + \beta_1 X_1 + \ldots + \beta_p X_p + \epsilon$$ 
# 
# * Back to the simple model. The model in linear regression is the *conditional mean* of $Y$ given the values in $X$ is expressed a linear function.  
# 
# $$ y = f(x) = E(Y | X = x)$$ 
# 
# ![conditional mean](images/conditionalmean.png)
# http://www.learner.org/courses/againstallodds/about/glossary.html
# 
# * The goal is to estimate the coefficients (e.g. $\beta_0$ and $\beta_1$). We represent the estimates of the coefficients with a "hat" on top of the letter.  
# 
# $$ \hat{\beta}_0, \hat{\beta}_1 $$
# 
# * Once you estimate the coefficients $\hat{\beta}_0$ and $\hat{\beta}_1$, you can use these to predict new values of $Y$
# 
# $$\hat{y} = \hat{\beta}_0 + \hat{\beta}_1 x_1$$
# 
# 
# * How do you estimate the coefficients? 
#     * There are many ways to fit a linear regression model
#     * The method called **least squares** is one of the most common methods
#     * We will discuss least squares today
#     
# ### Estimating $\hat\beta$: Least squares
# ***
# [Least squares](http://en.wikipedia.org/wiki/Least_squares) is a method that can estimate the coefficients of a linear model by minimizing the difference between the following: 
# 
# $$ S = \sum_{i=1}^N r_i = \sum_{i=1}^N (y_i - (\beta_0 + \beta_1 x_i))^2 $$
# 
# where $N$ is the number of observations.  
# 
# * We will not go into the mathematical details, but the least squares estimates $\hat{\beta}_0$ and $\hat{\beta}_1$ minimize the sum of the squared residuals $r_i = y_i - (\beta_0 + \beta_1 x_i)$ in the model (i.e. makes the difference between the observed $y_i$ and linear model $\beta_0 + \beta_1 x_i$ as small as possible). 
# 
# The solution can be written in compact matrix notation as
# 
# $$\hat\beta =  (X^T X)^{-1}X^T Y$$ 
# 
# We wanted to show you this in case you remember linear algebra, in order for this solution to exist we need $X^T X$ to be invertible. Of course this requires a few extra assumptions, $X$ must be full rank so that $X^T X$ is invertible, etc. **This is important for us because this means that having redundant features in our regression models will lead to poorly fitting (and unstable) models.** We'll see an implementation of this in the extra linear regression example.
# 
# **Note**: The "hat" means it is an estimate of the coefficient.  

# ***
# # Part 2: Boston Housing Data Set
# 
# The [Boston Housing data set](https://archive.ics.uci.edu/ml/datasets/Housing) contains information about the housing values in suburbs of Boston.  This dataset was originally taken from the StatLib library which is maintained at Carnegie Mellon University and is now available on the UCI Machine Learning Repository. 
# 
# 
# ## Load the Boston Housing data set from `sklearn`
# ***
# 
# This data set is available in the [sklearn](http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html#sklearn.datasets.load_boston) python module which is how we will access it today.  

# In[ ]:


from sklearn.datasets import load_boston
boston = load_boston()


# In[ ]:


boston.keys()


# In[ ]:


boston.data.shape


# In[ ]:


# Print column names
print boston.feature_names


# In[ ]:


# Print description of Boston housing data set
print boston.DESCR


# Now let's explore the data set itself. 

# In[ ]:


bos = pd.DataFrame(boston.data)
bos.head()


# There are no column names in the DataFrame. Let's add those. 

# In[ ]:


bos.columns = boston.feature_names
bos.head()


# Now we have a pandas DataFrame called `bos` containing all the data we want to use to predict Boston Housing prices.  Let's create a variable called `PRICE` which will contain the prices. This information is contained in the `target` data. 

# In[ ]:


print boston.target.shape


# In[ ]:


bos['PRICE'] = boston.target
bos.head()


# ## EDA and Summary Statistics
# ***
# 
# Let's explore this data set.  First we use `describe()` to get basic summary statistics for each of the columns. 

# In[ ]:


bos.describe()


# ### Scatter plots
# ***
# 
# Let's look at some scatter plots for three variables: 'CRIM', 'RM' and 'PTRATIO'. 
# 
# What kind of relationship do you see? e.g. positive, negative?  linear? non-linear? 

# In[ ]:


plt.scatter(bos.CRIM, bos.PRICE)
plt.xlabel("Per capita crime rate by town (CRIM)")
plt.ylabel("Housing Price")
plt.title("Relationship between CRIM and Price")


# In[ ]:


plt.scatter(bos.RM, bos.PRICE)
plt.xlabel("Average number of rooms per dwelling (RM)")
plt.ylabel("Housing Price")
plt.title("Relationship between RM and Price")

# sns.regplot(y="PRICE", x="RM", data=bos, fit_reg = True)


# In[ ]:


# We can also use seaborn regplot for this
#  This provides automatic linear regression fits (useful for data exploration later on)

sns.regplot(y="PRICE", x="RM", data=bos, fit_reg = True)


# In[ ]:


plt.scatter(bos.PTRATIO, bos.PRICE)
plt.xlabel("Pupil-to-Teacher Ratio (PTRATIO)")
plt.ylabel("Housing Price")
plt.title("Relationship between PTRATIO and Price")


# ### Histograms
# ***
# 

# In[ ]:


plt.hist(bos.CRIM)
plt.title("CRIM")
plt.xlabel("Crime rate per capita")
plt.ylabel("Frequencey")
plt.show()


# In[ ]:


plt.hist(bos.PRICE)
plt.title('Housing Prices: $Y_i$')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()


# ## Linear regression with  Boston housing data example
# ***
# 
# Here, 
# 
# $Y$ = boston housing prices (also called "target" data in python)
# 
# and
# 
# $X$ = all the other features (or independent variables)
# 
# which we will use to fit a linear regression model and predict Boston housing prices. We will use the least squares method as the way to estimate the coefficients.  

# We'll use two ways of fitting a linear regression. We recommend the first but the second is also powerful in its features.

# ### Fitting Linear Regression using `statsmodels`
# ***

# In[ ]:


# Import regression modules
# ols - stands for Ordinary least squares, we'll use this
import statsmodels.api as sm
from statsmodels.formula.api import ols


# In[ ]:


# statsmodels works nicely with pandas dataframes
# The thing inside the "quotes" is called a formula, a bit on that below
m = ols('PRICE ~ RM',bos).fit()
print m.summary()


# #### Interpreting coefficients
# 
# There is a ton of information in this output. But we'll concentrate on the coefficient table (middle table). We can interpret the `RM` coefficient (9.1021) by first noticing that the p-vale (under `P>|t|`) is so small, basically zero. We can interpret the coefficient as, if we compare two groups of towns, one where the average number of rooms is say $5$ and the other group is the same except that they all have $6$ rooms. For these two groups the average difference in house prives is about $9.1$ (in thousands) so about $\$9,100$ difference. The confidence interval fives us a range of plausible values for this difference, about ($\$8,279, \$9,925$), deffinitely not chump change. 
# 
# In the last section of this Lab we discuss p-values in more detail. Please have a read though it and ask your TFs for more help.

# ####  `statsmodels` formulas
# ***
# This formula notation will seem familiar to `R` users, but will take some getting used to for people coming from other languages or are new to statistics.
# 
# The formula gives instruction for a general structure for a regression call. For `statsmodels` (`ols` or `logit`) calls you need to have a Pandas dataframe with column names that you will add to your formula. In the below example you need a pandas data frame that includes the columns named (`Outcome`, `X1`,`X2`, ...), bbut you don't need to build a new dataframe for every regression. Use the same dataframe with all these things in it. The structure is very simple:
# 
# `Outcome ~ X1`
# 
# But of course we want to to be able to handle more complex models, for example multiple regression is doone like this:
# 
# `Outcome ~ X1 + X2 + X3`
# 
# This is the very basic structure but it should be enough to get you through the homework. Things can get much more complex, for a quick run-down of further uses see the `statsmodels` [help page](http://statsmodels.sourceforge.net/devel/example_formulas.html).
# 

# Let's see how our model actually fit our data. We can see below that there is a ceiling effect, we should probably look into that. Also, for large values of $Y$ we get underpredictions, most predictions are below the 45-degree gridlines. 

# In[ ]:


plt.scatter(bos['PRICE'], m.fittedvalues)
plt.xlabel("Prices: $Y_i$")
plt.ylabel("Predicted prices: $\hat{Y}_i$")
plt.title("Prices vs Predicted Prices: $Y_i$ vs $\hat{Y}_i$")


# ### Fitting Linear Regression using `sklearn`
# 

# In[ ]:


from sklearn.linear_model import LinearRegression
X = bos.drop('PRICE', axis = 1)

# This creates a LinearRegression object
lm = LinearRegression()
lm


# #### What can you do with a LinearRegression object? 

# In[ ]:


# Look inside linear regression object
# LinearRegression.<tab>


# Main functions | Description
# --- | --- 
# `lm.fit()` | Fit a linear model
# `lm.predit()` | Predict Y using the linear model with estimated coefficients
# `lm.score()` | Returns the coefficient of determination (R^2). *A measure of how well observed outcomes are replicated by the model, as the proportion of total variation of outcomes explained by the model*

# #### What output can you get?

# In[ ]:


# Look inside lm object
# lm.<tab>


# Output | Description
# --- | --- 
# `lm.coef_` | Estimated coefficients
# `lm.intercept_` | Estimated intercept 

# ### Fit a linear model
# ***
# 
# The `lm.fit()` function estimates the coefficients the linear regression using least squares. 

# In[ ]:


# Use all 13 predictors to fit linear regression model
lm.fit(X, bos.PRICE)

# your turn
# notice fit_intercept=True and normalize=True
# How would you change the model to not fit an intercept term? 


# ### Estimated intercept and coefficients
# 
# Let's look at the estimated coefficients from the linear model using `1m.intercept_` and `lm.coef_`.  
# 
# After we have fit our linear regression model using the least squares method, we want to see what are the estimates of our coefficients $\beta_0$, $\beta_1$, ..., $\beta_{13}$: 
# 
# $$ \hat{\beta}_0, \hat{\beta}_1, \ldots, \hat{\beta}_{13} $$
# 
# 

# In[ ]:


print 'Estimated intercept coefficient:', lm.intercept_


# In[ ]:


print 'Number of coefficients:', len(lm.coef_)


# In[ ]:


# The coefficients
pd.DataFrame(zip(X.columns, lm.coef_), columns = ['features', 'estimatedCoefficients'])


# ### Predict Prices 
# 
# We can calculate the predicted prices ($\hat{Y}_i$) using `lm.predict`. 
# 
# $$ \hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_1 + \ldots \hat{\beta}_{13} X_{13} $$

# In[ ]:


# first five predicted prices
lm.predict(X)[0:5]


# In[ ]:


plt.hist(lm.predict(X))
plt.title('Predicted Housing Prices (fitted values): $\hat{Y}_i$')
plt.xlabel('Price')
plt.ylabel('Frequency')


# Let's plot the true prices compared to the predicted prices to see they disagree, we saw this exactly befor but this is how you access the predicted values in using `sklearn`.

# In[ ]:


# plt.scatter(bos.PRICE, lm.predict(X))
# plt.xlabel("Prices: $Y_i$")
# plt.ylabel("Predicted prices: $\hat{Y}_i$")
# plt.title("Prices vs Predicted Prices: $Y_i$ vs $\hat{Y}_i$")


# ### Residual sum of squares
# 
# Let's calculate the residual sum of squares 
# 
# $$ S = \sum_{i=1}^N r_i = \sum_{i=1}^N (y_i - (\beta_0 + \beta_1 x_i))^2 $$

# In[ ]:


print np.sum((bos.PRICE - lm.predict(X)) ** 2)


# #### Mean squared error

# In[ ]:


mseFull = np.mean((bos.PRICE - lm.predict(X)) ** 2)
print mseFull


# ## Relationship between `PTRATIO` and housing price
# ***
# 
# Try fitting a linear regression model using only the 'PTRATIO' (pupil-teacher ratio by town)
# 
# Calculate the mean squared error. 
# 

# In[ ]:


lm = LinearRegression()
lm.fit(X[['PTRATIO']], bos.PRICE)


# In[ ]:


msePTRATIO = np.mean((bos.PRICE - lm.predict(X[['PTRATIO']])) ** 2)
print msePTRATIO


# We can also plot the fitted linear regression line. 

# In[ ]:


plt.scatter(bos.PTRATIO, bos.PRICE)
plt.xlabel("Pupil-to-Teacher Ratio (PTRATIO)")
plt.ylabel("Housing Price")
plt.title("Relationship between PTRATIO and Price")

plt.plot(bos.PTRATIO, lm.predict(X[['PTRATIO']]), color='blue', linewidth=3)
plt.show()


# # Your turn
# ***
# 
# Try fitting a linear regression model using three independent variables
# 
# 1. 'CRIM' (per capita crime rate by town)
# 2. 'RM' (average number of rooms per dwelling)
# 3. 'PTRATIO' (pupil-teacher ratio by town)
# 
# Calculate the mean squared error. 

# In[ ]:


# your turn


# 
# ## Other important things to think about when fitting a linear regression model
# ***
# <div class="span5 alert alert-danger">
# <ul>
#   <li>**Linearity**. The dependent variable $Y$ is a linear combination of the regression coefficients and the independent variables $X$. </li>
#   <li>**Constant standard deviation**. The SD of the dependent variable $Y$ should be constant for different values of X.  
#         <ul>
#             <li>e.g. PTRATIO
#         </ul>
#     </li>
#   <li> **Normal distribution for errors**.  The $\epsilon$ term we discussed at the beginning are assumed to be normally distributed. 
#   $$ \epsilon_i \sim N(0, \sigma^2)$$
# Sometimes the distributions of responses $Y$ may not be normally distributed at any given value of $X$.  e.g. skewed positively or negatively. </li>
# <li> **Independent errors**.  The observations are assumed to be obtained independently.
#     <ul>
#         <li>e.g. Observations across time may be correlated
#     </ul>
# </li>
# </ul>  
# 
# </div>
# 

# # Part 3: Training and Test Data sets
# 
# ### Purpose of splitting data into Training/testing sets
# ***
# <div class="span5 alert alert-info">
# 
# <p> Let's stick to the linear regression example: </p>
# <ul>
#   <li> We built our model with the requirement that the model fit the data well. </li>
#   <li> As a side-effect, the model will fit <b>THIS</b> dataset well. What about new data? </li>
#     <ul>
#       <li> We wanted the model for predictions, right?</li>
#     </ul>
#   <li> One simple solution, leave out some data (for <b>testing</b>) and <b>train</b> the model on the rest </li>
#   <li> This also leads directly to the idea of cross-validation, next section. </li>  
# </ul>
# </div>
# 
# ***
# 
# One way of doing this is you can create training and testing data sets manually. 

# In[ ]:


X_train = X[:-50]
X_test = X[-50:]
Y_train = bos.PRICE[:-50]
Y_test = bos.PRICE[-50:]
print X_train.shape
print X_test.shape
print Y_train.shape
print Y_test.shape


# Another way, is to split the data into random train and test subsets using the function `train_test_split` in `sklearn.cross_validation`. 

# In[ ]:


# let's look at the function in the help file
# sklearn.cross_validation.train_test_split?


# In[ ]:


X_train, X_test, Y_train, Y_test = sklearn.cross_validation.train_test_split(
    X, bos.PRICE, test_size=0.33, random_state = 5)
print X_train.shape
print X_test.shape
print Y_train.shape
print Y_test.shape


# Your turn.  Let's build a linear regression model using our new training data sets. 

# In[ ]:


# your turn
lm = LinearRegression()
lm.fit(X_train, Y_train)
pred_train = lm.predict(X_train)
pred_test = lm.predict(X_test)


# Now, calculate the mean squared error using just the test data and compare to mean squared from using all the data to fit the model. 

# In[ ]:


# your turn
print "Fit a model X_train, and calculate MSE with Y_train:", np.mean((Y_train - lm.predict(X_train)) ** 2)
print "Fit a model X_train, and calculate MSE with X_test, Y_test:", np.mean((Y_test - lm.predict(X_test)) ** 2)


# #### Residual plots

# In[ ]:


plt.scatter(lm.predict(X_train), lm.predict(X_train) - Y_train, c='b', s=40, alpha=0.5)
plt.scatter(lm.predict(X_test), lm.predict(X_test) - Y_test, c='g', s=40)
plt.hlines(y = 0, xmin=0, xmax = 50)
plt.title('Residual Plot using training (blue) and test (green) data')
plt.ylabel('Residuals')


# ### K-fold Cross-validation as an extension of this idea
# ***
# <div class="span5 alert alert-info">
# 
# <p> A simple extension of the Test/train split is called K-fold cross-validation.  </p>
# 
# <p> Here's the procedure:</p>
# <ul>
#   <li> randomly assign your $n$ samples to one of $K$ groups. They'll each have about $n/k$ samples</li>
#   <li> For each group $k$: </li>
#     <ul>
#       <li> Fit the model (e.g. run regression) on all data excluding the $k^{th}$ group</li>
#       <li> Use the model to predict the outcomes in group $k$</li>
#       <li> Calculate your prediction error for each observation in $k^{th}$ group (e.g. $(Y_i - \hat{Y}_i)^2$ for regression, $\mathbb{1}(Y_i = \hat{Y}_i)$ for logistic regression). </li>
#     </ul>
#   <li> Calculate the average prediction error across all samples $Err_{CV} = \frac{1}{n}\sum_{i=1}^n (Y_i - \hat{Y}_i)^2$ </li>
# </ul>
# </div>
# 
# ***
# 
# Luckily you don't have to do this entire process all by hand (``for`` loops, etc.) every single time, ``sci-kit learn`` has a very nice implementation of this, have a look at the [documentation](http://scikit-learn.org/stable/modules/cross_validation.html).

# ## Another Example: Old Faithful Geyser Data Set
# ***
# 
# The [Old Faithful Geyser](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/faithful.html) data set is a well-known data set that depicts the relationship of the waiting time between eruptions and the duration of the eruption for the Old Faithful geyser in Yellowstone National Park, Wyoming, USA [[webcam]](http://yellowstone.net/webcams/). This data set is found in the base installation of the [R programming language](http://cran.r-project.org).  
# 
# `faithful` is a data set with 272 observations on 2 variables.
# 
# Column name| Description 
# --- | --- 
# eruptions | Eruption time (in mins)
# waiting	| Waiting time to next eruption (in mins)
# 
# There is a function in `statsmodels` (or `sm` for short) called `sm.datasets.get_rdataset` which will download and return a data set found in [R](http://cran.r-project.org).  
# 
# Let's import the `faithful` dataset. 

# In[ ]:


faithful = sm.datasets.get_rdataset("faithful")


# In[ ]:


# Let's look at the help file
get_ipython().magic(u'pinfo sm.datasets.get_rdataset')
get_ipython().magic(u'pinfo faithful')


# In[ ]:


faithful.title


# In[ ]:


faithful = faithful.data
faithful.head()


# In[ ]:


faithful.shape


# ### Histogram 
# ***
# 
# Create a histogram of the time between eruptions. What do you see? 

# In[ ]:


plt.hist(faithful.waiting)
plt.xlabel('Waiting time to next eruption (in mins)')
plt.ylabel('Frequency')
plt.title('Old Faithful Geyser time between eruption')
plt.show()


# This histogram indicates [Old Faithful isn’t as “faithful” as you might think](http://people.stern.nyu.edu/jsimonof/classes/2301/pdf/geystime.pdf). 

# ### Scatter plot 
# ***
# 
# Create a scatter plot of the `waiting` on the x-axis and the `eruptions` on the y-axis. 

# In[ ]:


plt.scatter(faithful.waiting, faithful.eruptions)
plt.xlabel('Waiting time to next eruption (in mins)')
plt.ylabel('Eruption time (in mins)')
plt.title('Old Faithful Geyser')
plt.show()


# ### Build a linear regression to predict eruption time using `statsmodels`
# ***
# 
# Now let's build a linear regression model for the `faithful` DataFrame, and estimate the next eruption duration if the waiting time since the last eruption has been 75 minutes.
# 
# $$ Eruptions = \beta_0 + \beta_1 * Waiting + \epsilon $$ 

# In[ ]:


X = faithful.waiting
y = faithful.eruptions
model = sm.OLS(y, X)


# In[ ]:


# Let's look at the options in model
# model.<tab>


# In[ ]:


results = model.fit()


# In[ ]:


# Let's look at the options in results
# results.<tab>


# In[ ]:


print results.summary()


# In[ ]:


results.params.values


# We notice, there is no intercept ($\beta_0$) fit in this linear model.  To add it, we can use the function `sm.add_constant`.  

# In[ ]:


X = sm.add_constant(X)
X.head()


# Now let's fit a linear regression model with an intercept. 

# In[ ]:


modelW0 = sm.OLS(y, X)
resultsW0 = modelW0.fit()
print resultsW0.summary()


# If you want to predict the time to the next eruption using a waiting time of 75, you can directly estimate this using the equation 
# 
# $$ \hat{y} = \hat{\beta}_0 + \hat{\beta}_1 * 75 $$ 
# 
# or you can use `results.predict`.  

# In[ ]:


newX = np.array([1,75])
resultsW0.params[0]*newX[0] + resultsW0.params[1] * newX[1]


# In[ ]:


resultsW0.predict(newX)


# Based on this linear regression, if the waiting time since the last eruption has been 75 minutes, we expect the next one to last approximately 3.80 minutes.

# ### Plot the regression line 
# ***
# 
# Instead of using `resultsW0.predict(X)`, we can use `resultsW0.fittedvalues` which are the $\hat{y}$. 

# In[ ]:


plt.scatter(faithful.waiting, faithful.eruptions)
plt.xlabel('Waiting time to next eruption (in mins)')
plt.ylabel('Eruption time (in mins)')
plt.title('Old Faithful Geyser')

plt.plot(faithful.waiting, resultsW0.fittedvalues, color='blue', linewidth=3)
plt.show()


# ### Residuals, residual sum of squares, mean squared error
# ***
# 
# Recall, we can directly calculate the residuals as 
# 
# $$r_i = y_i - (\hat{\beta}_0 + \hat{\beta}_1 x_i)$$
# 
# To calculate the residual sum of squares, 
# 
# $$ S = \sum_{i=1}^n r_i = \sum_{i=1}^n (y_i - (\hat{\beta}_0 + \hat{\beta}_1 x_i))^2 $$
# 
# where $n$ is the number of observations.  Alternatively, we can simply ask for the residuals using `resultsW0.predict`

# In[ ]:


resids = faithful.eruptions - resultsW0.predict(X)


# In[ ]:


resids = resultsW0.resid


# In[ ]:


plt.plot(faithful.waiting, resids, 'o')
plt.hlines(y = 0, xmin=40, xmax = 100)
plt.xlabel('Waiting time')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()


# The residual sum of squares: 

# In[ ]:


print np.sum((faithful.eruptions - resultsW0.predict(X)) ** 2)


# Mean squared error: 

# In[ ]:


print np.mean((faithful.eruptions - resultsW0.predict(X)) ** 2)


# ## Build a linear regression to predict eruption time using least squares 
# ***
# 
# Now let's build a linear regression model for the `faithful` DataFrame, but instead of using `statmodels` (or `sklearn`), let's use the least squares estimates of the coefficients for the linear regression model.
# 
# $$ \hat{\beta} = (X^{\top}X)^{-1} X^{\top}Y $$ 
# 
# The `numpy` function [`np.dot`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.dot.html#numpy.dot) is the dot product (or inner product) of two vectors (or arrays in python).  
# 
# The `numpy` function [`np.linalg.inv`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.inv.html#numpy.linalg.inv) can be used to compute the inverse of a matrix. 

# In[ ]:


X = sm.add_constant(faithful.waiting)
y = faithful.eruptions


# First, compute $X^{\top}X$
# 

# In[ ]:


np.dot(X.T, X)


# Next, compute the inverse of $X^{\top}X$ or $(X^{\top}X)^{-1}$. 

# In[ ]:


np.linalg.inv(np.dot(X.T, X))


# Finally, compute $\hat{\beta} = (X^{\top}X)^{-1} X^{\top}Y $

# In[ ]:


beta = np.linalg.inv(np.dot(X.T, X)).dot(X.T).dot(y)
print "Directly estimating beta:", beta
print "Estimating beta using statmodels: ", resultsW0.params.values




# # Part 4: Many different types of regression
# ***
# <div class="span5 alert alert-info">
# 
# <p>You do not always have a continuous $y$ variable that you are measuring. Sometimes it may be binary (e.g. 0 or 1). Sometimes it may be count data.  What do you do?</p>
# 
# <p>Use other types of regression besides just simple linear regression.</p>  
# 
# <p>[Nice summary of several types of regression](http://www.datasciencecentral.com/profiles/blogs/10-types-of-regressions-which-one-to-use). </p>
# </div>
# 

# # Part 5: Logistic Regression
# ***
# 

# <div class="span5 alert alert-info">
# <p>Logistic regression is a probabilistic model that links observed binary data to a set of features.</p>
# 
# <p>Suppose that we have a set of binary (that is, taking the values 0 or 1) observations $Y_1,\cdots,Y_n$, and for each observation $Y_i$ we have a vector of features $X_i$. The logistic regression model assumes that there is some set of **weights**, **coefficients**, or **parameters** $\beta$, one for each feature, so that the data were generated by flipping a weighted coin whose probability of giving a 1 is given by the following equation:
# 
# $$
# P(Y_i = 1) = \mathrm{logistic}(\sum \beta_i X_i),
# $$
# 
# where
# 
# $$
# \mathrm{logistic}(x) = \frac{e^x}{1+e^x}.
# $$
# </p>
# <p>When we *fit* a logistic regression model, we determine values for each $\beta$ that allows the model to best fit the *training data* we have observed. Once we do this, we can use these coefficients to make predictions about data we have not yet observed.</p>
# 
# </div>

# From http://www.edwardtufte.com/tufte/ebooks, in "Visual and Statistical Thinking: 
# Displays of Evidence for Making Decisions":
# 
# >On January 28, 1986, the space shuttle Challenger exploded and seven astronauts died because two rubber O-rings leaked. These rings had lost their resiliency because the shuttle was launched on a very cold day. Ambient temperatures were in the low 30s and the O-rings themselves were much colder, less than 20F.
# 
# >One day before the flight, the predicted temperature for the launch was 26F to 29F. Concerned that the rings would not seal at such a cold temperature, the engineers who designed the rocket opposed launching Challenger the next day.
# 
# But they did not make their case persuasively, and were over-ruled by NASA.

# In[ ]:


from IPython.display import Image as Im
from IPython.display import display
Im('./images/shuttle.png')


# The image above shows the leak, where the O-ring failed.
# 
# We have here data on previous failures of the O-rings at various temperatures.

# In[ ]:


data=np.array([[float(j) for j in e.strip().split()] for e in open("./data/chall.txt")])
data


# Lets plot this data

# In[ ]:


# fit logistic regression model
import statsmodels.api as sm
from statsmodels.formula.api import logit, glm, ols

# statsmodels works nicely with pandas dataframes
dat = pd.DataFrame(data, columns = ['Temperature', 'Failure'])
logit_model = logit('Failure ~ Temperature',dat).fit()
print logit_model.summary()


# #### Interpreting p-values:
# Generally we'd like the p-values to be very small as they represent the probability that we observed such an strong relationship between temperature and O-ring failures purely by chance. So when the p-value is small (we usually consider "small" as less than 0.05), what we're saying is that based on the data we observed, we know **fairly certainly** that temperature is strongly associated with the failure of O-rings. This is a very powerful statement that can take us a long way in terms of learning if used properly. Have a look at the Wikipedia page on [p-values](https://en.wikipedia.org/wiki/P-value) for a quick reminder.
# 
# There are some issues with testing many many hypotheses that we'll also encounter in the homework. But generally, the idea is that the data may (or may not) have information about things you're interested in. We ask the data questions through hypotheses, but the more questions we ask of it, the higher chances we have of the data actually showing associations at random. Have alook at [this article](https://en.wikipedia.org/wiki/Multiple_comparisons_problem) to get an idea of the problem and some solutions. We'll be considering a very crude solution known as the [Bonferroni correction](https://en.wikipedia.org/wiki/Bonferroni_correction) but that is by no means the best solution. 

# In[ ]:


# calculate predicted failure probabilities for new termperatures
x = np.linspace(50, 85, 1000)
p = logit_model.params
eta = p['Intercept'] + x*p['Temperature']
y = np.exp(eta)/(1 + np.exp(eta))


# Let's plot the data along with a range of predicted failure probabilities for unobserved temperatures.

# In[ ]:


# plot data
temps, pfail = data[:,0], data[:,1]
plt.scatter(temps, pfail)
axes=plt.gca()
plt.xlabel('Temperature')
plt.ylabel('Failure')
plt.title('O-ring failures')

# plot fitted values
plt.plot(x, y)

# change limits, for a nicer plot
plt.xlim(50, 85)
plt.ylim(-0.1, 1.1)


# We can interpret the output from a logistic regression by looking at the coefficient of temperature (as well as the p-value). Since the coefficient of temperature is negative, we can say that an increase in temperature is associated with a decrease in the odds of having an O-ring failure. 