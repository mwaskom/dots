import pandas as pd
from psychopy import core
from visigoth import AcquireFixation, AcquireTarget, flexible_values
from visigoth.stimuli import RandomDotMotion, Point, Points


def create_stimuli(exp):

    fix = Point(exp.win,
                exp.p.fix_pos,
                exp.p.fix_radius,
                exp.p.fix_color)

    # Saccade targets
    targets = Points(exp.win,
                     exp.p.target_pos,
                     exp.p.target_radius,
                     exp.p.target_color)

    dots = RandomDotMotion(exp.win,
                           aperture=exp.p.aperture_size,
                           pos=exp.p.aperture_pos,
                           size=exp.p.dot_size
                           )

    return locals()


def generate_trials(exp):

    for _ in exp.trial_count(max=exp.p.trials_per_run):

        target = flexible_values(range(len(exp.p.dot_dir)))

        t_info = exp.trial_info(

            iti=flexible_values(exp.p.wait_iti),
            wait_pre_stim=flexible_values(exp.p.wait_pre_stim),
            dot_coh=flexible_values(exp.p.dot_coh),
            dot_dir=exp.p.dot_dir[target],
            target=target,

            )

        yield t_info


def run_trial(exp, info):

    # Inter-trial interval
    exp.wait_until(exp.iti_end, iti_duration=info["iti"])

    # Wait for trial onset
    exp.tracker.send_message("start trial {}".format(info["trial"]))
    info["fp_on"] = exp.clock.getTime()
    exp.tracker.send_message("fp_on")
    res = exp.wait_until(AcquireFixation(exp),
                         timeout=exp.p.wait_fix,
                         draw="fix")

    if res is None:
        info["result"] = "nofix"
        exp.sounds.nofix.play()
        return info

    # Show the targets
    info["targ_on"] = exp.clock.getTime()
    exp.tracker.send_message("targ_on")
    res = exp.wait_until(timeout=info["wait_pre_stim"],
                         draw=["fix", "targets"],
                         check_abort=True)

    # Show the stimulus
    rt_clock = core.Clock()
    for i in exp.frame_range(seconds=exp.p.wait_resp):

        exp.s.dots.update(info["dot_dir"], info["dot_coh"])
        exp.draw(["fix", "targets", "dots"])

        if not i:
            info["dots_on"] = exp.clock.getTime()
            exp.tracker.send_message("dots_on")

        if not exp.check_fixation():
            rt = rt_clock.getTime()
            info["dots_off"] = exp.clock.getTime()
            exp.tracker.send_message("dots_off")
            res = exp.wait_until(AcquireTarget(exp, info["target"]),
                                 draw="targets")
            break

    else:
        res = None

    # Handle the response
    if res is None:
        info["result"] = "fixbreak"
    else:
        info.update(pd.Series(res))

    # Inject the estimated RT
    if info["responded"]:
        info["rt"] = rt

    # Give feedback
    info["fb_on"] = exp.clock.getTime()
    exp.tracker.send_message("fb on")
    exp.sounds[info["result"]].play()
    exp.show_feedback("targets", info["result"], info["response"])
    exp.wait_until(timeout=exp.p.wait_feedback, draw="targets")
    exp.s.targets.color = exp.p.target_color

    exp.tracker.send_message("end trial {}".format(info["trial"]))

    return info
