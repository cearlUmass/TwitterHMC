import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
import arviz as az
import xarray as xr



def main():

    ob1 = np.array(np.random.normal(loc=10, scale=1, size=100))
    ob2 = np.array(np.random.normal(loc=-10, scale=1, size=100))
    observed = np.concatenate([ob1, ob2])
    az.plot_posterior(observed)
    plt.show()

    model = pm.Model()
    with model:

        # Priors
        loc1 = pm.Normal("loc", mu=10, sigma=20)
        size1 = pm.HalfNormal("size", sigma=2)
        # loc2 = pm.Normal("loc1", mu=0, sigma=2)
        # size2 = pm.Normal("size1", mu=0, sigma=2)

        # Likelihood of observations
        y_obs = pm.Normal("y_obs", mu=loc1, sigma=size1, observed=observed)

    with model:
        trace = pm.sample(100, cores=4, init='adapt_diag')
        az.to_netcdf(trace, "trace")
        az.plot_trace(trace)
        plt.show()

    print(trace.report)


    # i = 2
    # j = 3
    # g = 1
    #
    # x = tt._shared(np.arange(i))
    # y = tt._shared(np.arange(j))
    #
    # x_M = pm.math.stack([x for k in range(j)], axis=1)
    # y_M = pm.math.stack([y for k in range(i)]) * g
    # print(x_M.eval())
    # print(y_M.eval())

    # z = tt._shared(np.array((np.arange(1, 10), np.arange(1, 10))))
    # z = tt.pow(z, (np.arange(1,10)))
    # print(z.eval())


if __name__ == '__main__':
    main()