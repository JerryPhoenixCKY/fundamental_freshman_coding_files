# Principle of algorithm analysis 1: Counting primitive operations
#
# • To analyse the running time of an algorithm without performing
# experiments, we perform an analysis directly on a high-level description of
# the algorithm
#
# • We define a set of primitive operations such as the following:
# ✓ Assigning an variable to an object
# ✓ Determining the object associated with an variable
# ✓ Performing an arithmetic operation (for example, adding two numbers)
# ✓ Comparing two numbers
# ✓ Accessing a single element of a Python list by index
# ✓ Calling a function (excluding operations executed within the function)
# ✓ Returning from a function.
#
#
# Principle of algorithm analysis 2: Measuring Operations as a Function of Input Size
#
# • To capture the order of growth of an algorithm’s running
# time, we will associate, with each algorithm, a function f (n)
# that characterizes the number of primitive operations that
# are performed as a function of the problem size n
#
# Principle of algorithm analysis 3: Focusing on the Worst-Case Input
#  We may use the following 7 functions to measure the time complexity of an algorithm:
# constant,
# logarithm
# linear
# N-log-N
# quadratic
# cubic
# other polynomials, exponential
