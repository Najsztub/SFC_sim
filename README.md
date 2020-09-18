# Macroeconomic modelling using SFC approach

I try to replicate the analysis from [Monetary Economics, An Integrated Approach to Credit,Money, Income, Production and Wealth](https://www.amazon.com/Monetary-Economics-Integrated-Approach-Production/dp/0230301843) by W. Godley and M. Lavoie. I started with writing a simple Python class to make modelling easier. 

On first reading I find the SFC (Stock-Flow Consistent) approach appealing. It makes variables explainable, not coming out of the blue. Moreover it treats money as endogenous. 

In this approach I simply create a list of functions that are being run in each step. The functions operate on local Namespace, so that I can reference time-dependent variables simply as X(t) with `X` being the variable and `t` being time. 