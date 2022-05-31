#include <cmath>
#include <vector>

#include <iostream>
using namespace std;



vector<vector<double>> top_relaxation(int _N, int _M, vector<double> _xs, vector<double> _ys, double _w, int _n_max, double _eps)
{
    int N, M, n_max;
    double w, eps, h2, k2, a2;
    vector<double> xs;
    vector<double> ys;
    vector<vector<double>> grid;

    N = _N;
    M = _M;
    n_max = _n_max;
    w = _w;
    eps = _eps;
    xs = _xs;
    ys = _ys;
    h2 = N * N / 4;
    k2 = M * M / 4;
    a2 = -2 * (h2 + k2);


    //resize grid and approximate
    grid.resize(M+2);
    for (int j = 0; j < M+2; j++)
    {
        grid[j].resize(N+1);
        for (int i = 0; i < N+1; i++)
        {
            grid[j][i] = 0;
        }
    }


    //solve Left Right Columns
    for (int j = 0; j < M + 1; j++)
    {
        grid[j][N] = exp(ys[j]) * (1.0 - ys[j] * ys[j]);
        grid[j][0] = 1.0 - ys[j] * ys[j];
    }

    //solve Bottom Top Rows
    for (int i = 0; i < N + 1; i++)
    {
        grid[M][i] = 1.0 - xs[i] * xs[i];
        grid[0][i] = 1.0 - xs[i] * xs[i];
    }

    //solve Centre of grid
    int n = 0;
    double eps_n = 0;
    while (true)
    {
        double eps_max = 0;

        for (int j = 1; j < M; j++)
        {
            for (int i = 1; i < N; i++)
            {
                double v_old = grid[j][i];

                double temp = a2 * v_old + h2 * (grid[j][i + 1] + grid[j][i - 1]) + k2 * (grid[j + 1][i] + grid[j - 1][i]);
                double v_new = v_old - w * (temp + abs(xs[i] * xs[i] - ys[j] * ys[j])) / a2;

                grid[j][i] = v_new;

                double eps_curr = abs(v_old - v_new);
                if (eps_curr > eps_max)
                {
                    eps_max = eps_curr;
                };
            }
        }

        n++;
        if ((eps_max < eps) || (n >= n_max))
        {
            eps_n = eps_max;
            break;
        };
    }

    double R_max = 0;
    for (int j = 1; j < M; j++)
    {
        for (int i = 1; i < N; i++)
        {
            double R = abs(a2 * grid[j][i] + h2 * (grid[j][i + 1] + grid[j][i - 1]) + k2 * (grid[j + 1][i] + grid[j - 1][i])
                + abs(xs[i] * xs[i] - ys[j] * ys[j]));
            if (R > R_max) R_max = R;
        }
    }

    grid[M + 1][0] = double(n);
    grid[M + 1][1] = eps_n;
    grid[M + 1][2] = R_max;

    return grid;
}


vector<vector<double>> top_relaxation_test(int _N, int _M, vector<double> _xs, vector<double> _ys, double _w, int _n_max, double _eps)
{
    int N, M, n_max;
    double w, eps, h2, k2, a2;
    vector<double> xs;
    vector<double> ys;
    vector<vector<double>> grid;

    N = _N;
    M = _M;
    n_max = _n_max;
    w = _w;
    eps = _eps;
    xs = _xs;
    ys = _ys;
    h2 = N * N / 4;
    k2 = M * M / 4;
    a2 = -2 * (h2 + k2);


    //resize grid from bottom to top from left to right and approximate
    grid.resize(M + 2);
    for (int j = 0; j < M + 2; j++)
    {
        grid[j].resize(N + 1);
        for (int i = 0; i < N + 1; i++)
        {
            grid[j][i] = 0;
        }
    }


    //solve Left Right Columns
    for (int j = 0; j < M + 1; j++)
    {
        grid[j][N] = exp(-ys[j] * ys[j]);
        grid[j][0] = exp(-ys[j] * ys[j]);
    }

    //solve Bottom Top Rows
    for (int i = 0; i < N + 1; i++)
    {
        grid[M][i] = exp(-xs[i] * xs[i]);
        grid[0][i] = exp(-xs[i] * xs[i]);
    }

    //solve Centre of grid
    int n = 0;
    double eps_n = 0;
    while (true)
    {
        double eps_max = 0;

        for (int j = 1; j < M; j++)
        {
            for (int i = 1; i < N; i++)
            {
                double v_old = grid[j][i];

                double temp = a2 * v_old + h2 * (grid[j][i + 1] + grid[j][i - 1]) + k2 * (grid[j + 1][i] + grid[j - 1][i]);
                double v_new = v_old - w * (temp + 4.0 * (1.0 - xs[i] * xs[i] - ys[j] * ys[j]) * exp(1.0 - xs[i] * xs[i] - ys[j] * ys[j])) / a2;

                grid[j][i] = v_new;

                double eps_curr = abs(v_old - v_new);
                if (eps_curr > eps_max)
                {
                    eps_max = eps_curr;
                };
            }
        }

        n++;
        if ((eps_max < eps) || (n >= n_max))
        {
            eps_n = eps_max;
            break;
        };
    }

    double R_max = 0;
    for (int j = 1; j < M; j++)
    {
        for (int i = 1; i < N; i++)
        {
            double R = abs(a2 * grid[j][i] + h2 * (grid[j][i + 1] + grid[j][i - 1]) + k2 * (grid[j + 1][i] + grid[j - 1][i])
                + 4.0 * exp(1.0 - xs[i] * xs[i] - ys[j] * ys[j]) * (1.0 - xs[i] * xs[i] - ys[j] * ys[j]));
            if (R > R_max) R_max = R;
        }
    }

    grid[M + 1][0] = double(n);
    grid[M + 1][1] = eps_n;
    grid[M + 1][2] = R_max;

    return grid;
}


double tau_md(int _N, int _M, vector<vector<double>> _r, double _a2, double _h2, double _k2)
{
    int N = _N;
    int M = _M;
    double tau = 0.0;
    double h2 = _h2;
    double k2 = _k2;
    double a2 = _a2;
    vector<vector<double>> r = _r;
    vector<vector<double>> Ar;

    Ar.resize(M + 1);
    for (int j = 0; j < M + 1; j++)
    {
        Ar[j].resize(N + 1);
        for (int i = 0; i < N + 1; i++)
        {
            Ar[j][i] = 0;
        }
    }


    for (int j = 2; j < M - 1 ; j++)
    {
        for (int i = 2; i < N - 1; i++)
        {
            Ar[j][i] = a2 * r[j][i] + h2 * (r[j][i + 1] + r[j][i - 1]) + k2 * (r[j + 1][i] + r[j - 1][i]);
        }
    }

    for (int j = 2; j < M - 1; j++)
    {
        Ar[j][1] = a2 * r[j][1] + h2 * r[j][2] + k2 * (r[j + 1][1] + r[j - 1][1]);
        Ar[j][N - 1] = a2 * r[j][N - 1] + h2 * r[j][N - 2] + k2 * (r[j + 1][N - 1] + r[j - 1][N - 1]);
    }

    for (int i = 2; i < N - 1; i++)
    {
        Ar[1][i] = a2 * r[1][i] + h2 * (r[1][i + 1] + r[1][i - 1]) + k2 * r[2][i];
        Ar[M - 1][i] = a2 * r[M - 1][i] + h2 * (r[M - 1][i + 1] + r[M - 1][i - 1]) + k2 * r[M - 2][i];
    }

    Ar[1][1] = a2 * r[1][1] + h2 * r[1][2] + k2 * r[2][1];
    Ar[1][N - 1] = a2 * r[1][N - 1] + h2 * r[1][N - 2] + k2 * r[2][N - 1];
    Ar[M-1][1] = a2 * r[M-1][1] + h2 * r[M - 1][2] + k2 * r[M - 2][1];
    Ar[M - 1][N - 1] = a2 * r[M - 1][N - 1] + h2 * r[M - 1][N - 2] + k2 * r[M - 2][N - 1];

    double Ar_r = 0.0;
    for (int j = 1; j < M; j++)
    {
        for (int i = 1; i < N; i++)
        {
            Ar_r += Ar[j][i] * r[j][i];
        }
    }

    double Ar_Ar = 0.0;
    for (int j = 1; j < M; j++)
    {
        for (int i = 1; i < N; i++)
        {
            Ar_Ar += Ar[j][i] * Ar[j][i];
        }
    }

    tau = Ar_r / Ar_Ar;

    return tau;
}


vector<vector<double>> min_discrepancies_test(int _N, int _M, vector<double> _xs, vector<double> _ys, int _n_max, double _eps)
{
    int N, M, n_max;
    double eps, h2, k2, a2;
    vector<double> xs;
    vector<double> ys;
    vector<vector<double>> v;
    vector<vector<double>> r;

    N = _N;
    M = _M;
    n_max = _n_max;
    eps = _eps;
    xs = _xs;
    ys = _ys;
    h2 = N * N / 4;
    k2 = M * M / 4;
    a2 = -2 * (h2 + k2);


    //resize grid from bottom to top from left to right and approximate
    v.resize(M + 2);
    r.resize(M + 2);
    for (int j = 0; j < M + 2; j++)
    {
        v[j].resize(N + 1);
        r[j].resize(N + 1);
        for (int i = 0; i < N + 1; i++)
        {
            v[j][i] = 0;
            r[j][i] = 0;
        }
    }


    //solve Left Right Columns
    for (int j = 0; j < M + 1; j++)
    {
        v[j][N] = exp(-ys[j] * ys[j]);
        v[j][0] = exp(-ys[j] * ys[j]);
    }

    //solve Bottom Top Rows
    for (int i = 0; i < N + 1; i++)
    {
        v[M][i] = exp(-xs[i] * xs[i]);
        v[0][i] = exp(-xs[i] * xs[i]);
    }

    //solve Centre of grid
    int n = 0;
    double eps_n = 0;

    for (int j = 1; j < M; j++)
    {
        for (int i = 1; i < N; i++)
        {
            r[j][i] = a2 * v[j][i] + h2 * (v[j][i + 1] + v[j][i - 1]) + k2 * (v[j + 1][i] + v[j - 1][i])
                + 4.0 * exp(1.0 - xs[i] * xs[i] - ys[j] * ys[j]) * (1.0 - xs[i] * xs[i] - ys[j] * ys[j]);
        }
    }

    while (true)
    {
        double eps_max = 0;
        double tau = tau_md(N, M, r, a2, h2, k2);

        for (int j = 1; j < M; j++)
        {
            for (int i = 1; i < N; i++)
            {
                double v_old = v[j][i];

                double v_new = v_old - tau * r[j][i];

                v[j][i] = v_new;

                double eps_curr = abs(v_old - v_new);
                if (eps_curr > eps_max)
                {
                    eps_max = eps_curr;
                };
            }
        }

        for (int j = 1; j < M; j++)
        {
            for (int i = 1; i < N; i++)
            {
                r[j][i] = a2 * v[j][i] + h2 * (v[j][i + 1] + v[j][i - 1]) + k2 * (v[j + 1][i] + v[j - 1][i])
                    + 4.0 * exp(1.0 - xs[i] * xs[i] - ys[j] * ys[j]) * (1.0 - xs[i] * xs[i] - ys[j] * ys[j]);
            }
        }

        n++;
        if ((eps_max < eps) || (n >= n_max))
        {
            eps_n = eps_max;
            break;
        };
    }

    double R_max = 0;
    for (int j = 1; j < M; j++)
    {
        for (int i = 1; i < N; i++)
        {
            double R = abs(a2 * v[j][i] + h2 * (v[j][i + 1] + v[j][i - 1]) + k2 * (v[j + 1][i] + v[j - 1][i])
                + 4.0 * exp(1.0 - xs[i] * xs[i] - ys[j] * ys[j]) * (1.0 - xs[i] * xs[i] - ys[j] * ys[j]));
            if (R > R_max) R_max = R;
        }
    }

    v[M + 1][0] = double(n);
    v[M + 1][1] = eps_n;
    v[M + 1][2] = R_max;

    return v;
}


vector<vector<double>> min_discrepancies(int _N, int _M, vector<double> _xs, vector<double> _ys, int _n_max, double _eps)
{
    int N, M, n_max;
    double eps, h2, k2, a2;
    vector<double> xs;
    vector<double> ys;
    vector<vector<double>> v;
    vector<vector<double>> r;

    N = _N;
    M = _M;
    n_max = _n_max;
    eps = _eps;
    xs = _xs;
    ys = _ys;
    h2 = N * N / 4;
    k2 = M * M / 4;
    a2 = -2 * (h2 + k2);


    //resize grid from bottom to top from left to right and approximate
    v.resize(M + 2);
    r.resize(M + 2);
    for (int j = 0; j < M + 2; j++)
    {
        v[j].resize(N + 1);
        r[j].resize(N + 1);
        for (int i = 0; i < N + 1; i++)
        {
            v[j][i] = 0;
            r[j][i] = 0;
        }
    }


    //solve Left Right Columns
    for (int j = 0; j < M + 1; j++)
    {
        v[j][N] = exp(ys[j]) * (1.0 - ys[j] * ys[j]);
        v[j][0] = 1.0 - ys[j] * ys[j];
    }

    //solve Bottom Top Rows
    for (int i = 0; i < N + 1; i++)
    {
        v[M][i] = 1.0 - xs[i] * xs[i];
        v[0][i] = 1.0 - xs[i] * xs[i];
    }

    //solve Centre of grid
    int n = 0;
    double eps_n = 0;

    for (int j = 1; j < M; j++)
    {
        for (int i = 1; i < N; i++)
        {
            r[j][i] = a2 * v[j][i] + h2 * (v[j][i + 1] + v[j][i - 1]) + k2 * (v[j + 1][i] + v[j - 1][i])
                + abs(xs[i] * xs[i] - ys[j] * ys[j]);
        }
    }

    while (true)
    {
        double eps_max = 0;
        double tau = tau_md(N, M, r, a2, h2, k2);

        for (int j = 1; j < M; j++)
        {
            for (int i = 1; i < N; i++)
            {
                double v_old = v[j][i];

                double v_new = v_old - tau * r[j][i];

                v[j][i] = v_new;

                double eps_curr = abs(v_old - v_new);
                if (eps_curr > eps_max)
                {
                    eps_max = eps_curr;
                };
            }
        }

        for (int j = 1; j < M; j++)
        {
            for (int i = 1; i < N; i++)
            {
                r[j][i] = a2 * v[j][i] + h2 * (v[j][i + 1] + v[j][i - 1]) + k2 * (v[j + 1][i] + v[j - 1][i])
                    + abs(xs[i] * xs[i] - ys[j] * ys[j]);
            }
        }

        n++;
        if ((eps_max < eps) || (n >= n_max))
        {
            eps_n = eps_max;
            break;
        };
    }

    double R_max = 0;
    for (int j = 1; j < M; j++)
    {
        for (int i = 1; i < N; i++)
        {
            double R = abs(a2 * v[j][i] + h2 * (v[j][i + 1] + v[j][i - 1]) + k2 * (v[j + 1][i] + v[j - 1][i])
                + abs(xs[i] * xs[i] - ys[j] * ys[j]));
            if (R > R_max) R_max = R;
        }
    }

    v[M + 1][0] = double(n);
    v[M + 1][1] = eps_n;
    v[M + 1][2] = R_max;

    return v;
}


int main()
{
    vector<vector<double>> grid;
    vector<double> xs;
    vector<double> ys;
    xs.resize(513);
    ys.resize(513);

    double k = -1.0;
    for(int i = 0; i < 512+1; i++)
    {
        xs[i] = k;
        ys[i] = k;
        k += 0.00390625;
    }

    grid = min_discrepancies(512, 512, xs, ys, 10, pow(10, -10));
    cout << "Iterations = " << grid[513][0] << endl
        << "Eps(method) = " << grid[513][1] << endl
        << "R = " << grid[513][2] << endl;

    cout << "v table:" << endl;

    for (int j = 256 - 4; j < 256 + 4 + 1; j++)
    {
        for (int i = 256 - 4; i < 256 + 4 + 1; i++)
        {
            cout.width(15);
            cout << grid[512-j][i] << " ";
        }
        cout << endl;
    }

    //cout << "u(0, 0) = " << exp(1 - xs[128] * xs[128] - ys[128] * ys[128]);
    //cout << endl;
    //cout << grid[128][128] - exp(1 - xs[128] * xs[128] - ys[128] * ys[128]) << endl;
    cout << "x = " << xs[256] << " y = " << ys[256];

    return 0;
}
/*
*/