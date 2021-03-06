.. _continuous-chi:

Chi Distribution
================

Generated by taking the (positive) square-root of chi-squared
variates.

.. math::
:nowrap:

        \begin{eqnarray*} f\left(x;\nu\right) & = & \frac{x^{\nu-1}e^{-x^{2}/2}}{2^{\nu/2-1}\Gamma\left(\frac{\nu}{2}\right)}I_{\left(0,\infty\right)}\left(x\right)\\ F\left(x;\nu\right) & = & \Gamma\left(\frac{\nu}{2},\frac{x^{2}}{2}\right)\\ G\left(\alpha;\nu\right) & = & \sqrt{2\Gamma^{-1}\left(\frac{\nu}{2},\alpha\right)}\end{eqnarray*}

.. math::

     M\left(t\right)=\Gamma\left(\frac{v}{2}\right)\,_{1}F_{1}\left(\frac{v}{2};\frac{1}{2};\frac{t^{2}}{2}\right)+\frac{t}{\sqrt{2}}\Gamma\left(\frac{1+\nu}{2}\right)\,_{1}F_{1}\left(\frac{1+\nu}{2};\frac{3}{2};\frac{t^{2}}{2}\right)

.. math::
:nowrap:

        \begin{eqnarray*} \mu & = & \frac{\sqrt{2}\Gamma\left(\frac{\nu+1}{2}\right)}{\Gamma\left(\frac{\nu}{2}\right)}\\ \mu_{2} & = & \nu-\mu^{2}\\ \gamma_{1} & = & \frac{2\mu^{3}+\mu\left(1-2\nu\right)}{\mu_{2}^{3/2}}\\ \gamma_{2} & = & \frac{2\nu\left(1-\nu\right)-6\mu^{4}+4\mu^{2}\left(2\nu-1\right)}{\mu_{2}^{2}}\\ m_{d} & = & \sqrt{\nu-1}\quad\nu\geq1\\ m_{n} & = & \sqrt{2\Gamma^{-1}\left(\frac{\nu}{2},\frac{1}{2}\right)}\end{eqnarray*}

Implementation: `scipy.stats.chi`
