import numpy as np
import xpart as xp
import xtrack as xt

def initial_conditions_grid(
    study,
    energy_spread,
    ini_cond_type=None,
    min_y_r=None,
    max_y_r=None,
    nn_y_r=None,
    min_x_theta=None,
    max_x_theta=None,
    nn_x_theta=None,
    delta_initial_values=None,
):
    if min_y_r is None:
        if study in ["DA", "MA"]:
            min_y_r = 0

    if max_y_r is None:
        if study == "DA":
            max_y_r = 50
        elif study == "MA":
            max_y_r = 30

    if nn_y_r is None:
        if study == "DA":
            nn_y_r = 51
        elif study == "MA":
            nn_y_r = 31

    if min_x_theta is None:
        if study == "DA":
            min_x_theta = -20
        elif study == "MA":
            min_x_theta = np.pi / 4

    if max_x_theta is None:
        if study == "DA":
            max_x_theta = 20
        elif study == "MA":
            max_x_theta = np.pi / 4

    if nn_x_theta is None:
        if study == "DA":
            nn_x_theta = 41
        elif study == "MA":
            nn_x_theta = 1

    if delta_initial_values is None:
        if study == "DA":
            delta_initial_values = 0
        elif study == "MA":
            delta_initial_values = np.linspace(
                -35 * energy_spread, 35 * energy_spread, 51
            )

    if study == "DA":
        if ini_cond_type is None or ini_cond_type == "cartesian":
            x_norm_points = np.linspace(min_x_theta, max_x_theta, nn_x_theta)
            y_norm_points = np.linspace(min_y_r, max_y_r, nn_y_r)
            x_norm_grid, y_norm_grid = np.meshgrid(x_norm_points, y_norm_points)
            x_normalized = x_norm_grid.flatten()
            y_normalized = y_norm_grid.flatten()

        elif ini_cond_type == "polar":
            x_normalized, y_normalized, r_xy, theta_xy = xp.generate_2D_polar_grid(
                r_range=(min_y_r, max_y_r),  # beam sigmas
                theta_range=(min_x_theta, max_x_theta),
                nr=nn_y_r,
                ntheta=nn_x_theta,
            )

    if study == "MA":
        if ini_cond_type is None or ini_cond_type == "polar":
            x_normalized, y_normalized, r_xy, theta_xy = xp.generate_2D_polar_grid(
                r_range=(min_y_r, max_y_r),  # beam sigmas
                theta_range=(min_x_theta, max_x_theta),
                nr=nn_y_r,
                ntheta=nn_x_theta,
            )

        elif ini_cond_type == "cartesian":
            x_norm_points = np.linspace(min_x_theta, max_x_theta, nn_x_theta)
            y_norm_points = np.linspace(min_y_r, max_y_r, nn_y_r)
            x_norm_grid, y_norm_grid = np.meshgrid(x_norm_points, y_norm_points)
            x_normalized = x_norm_grid.flatten()
            y_normalized = y_norm_grid.flatten()

    if study in ["DA", "MA"]:
        num_delta = np.size(delta_initial_values)
        num_particles = num_delta * nn_x_theta * nn_y_r
        if num_delta != 1:
            x_normalized = np.tile(x_normalized, num_delta)
            y_normalized = np.tile(y_normalized, num_delta)
            delta_init = np.repeat(
                delta_initial_values, np.size(x_normalized) / num_delta
            )
        else:
            delta_init = delta_initial_values

    if study == "Lifetime":
        num_particles = 500
        x_normalized = np.nan
        y_normalized = np.nan
        delta_init = np.nan
        nn_x_theta = np.nan
        nn_y_r = np.nan
        num_delta = np.nan

    out = xt.Table(dict(
        id=np.arange(num_particles, dtype=int),
        x_normalized = x_normalized,
        y_normalized = y_normalized,
        delta_init = delta_init
        ),
        index='id'
        )
    out.nn_x_theta = nn_x_theta,
    out.nn_y_r = nn_y_r,
    out.num_delta = num_delta,
    out.num_particles = num_particles

    return out