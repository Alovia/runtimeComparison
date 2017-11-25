# runtimeComparison
Little script to check how your algorithm matches up to your analysis when you actually run it on your computer.

I'm not very happy with it yet, but what you see is what you get.

# Why I wrote this:
#
# 1. I'm suspicious of how much overhead python adds.  2x?  3x? when
#    compared to C.  At what point does a shared library become
#    attractive?
#
# 2. It's one thing to analyse an algorithm, but yet another to check.
#    so the idea is that this program provides an approximate benchmark
#    to compare the result of the analysis to.
#
# 3. I'm not sure about bogomips.  They sound bogus.  As bogus as the
#    math in this little toy.  Seriously, so far, nothing works quite
#    out, I can get (say) the expected O(n) very close to the actual
#    time but the times for the actual O(log n) and O(n^2) wildly
#    differ from the expected results.  I am not sure what is going on.
#
# 4. It was inspired by an exercise in the big white Algo book I have
#    that has an MIT video course to go with it.  Why compile a list
#    by hand, if you can make the computer do it for you? :-)
