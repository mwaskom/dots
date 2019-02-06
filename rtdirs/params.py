
base = dict(

    display_name="kianilab-ps1",
    display_luminance=25,

    target_pos=[(-10, 0), (+10, 0)],

    dot_coh=[0, .016, .032, .064, .128, .256, .512],
    dot_dir=[180, 0],
    dot_size=.1,

    aperture_pos=(0, 0),
    aperture_size=5,

    wait_pre_stim=("truncexpon", 4, 1, .25),

    monitor_eye=True,
    eye_fixation=True,
    eye_response=True,

    wait_iti=2,

    trials_per_run=250,
    perform_acc_target=.82,
    perform_rt_target=1,

    output_template="data/{subject}/{session}/dirs_{time}",

)
