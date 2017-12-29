from . import calc_filmsize

engine_to_str = {
    "PATHCPU": "Path CPU",
    "PATHOCL": "Path OpenCL",
    "TILEPATHCPU": "Tile Path CPU",
    "TILEPATHOCL": "Tile Path OpenCL",
    "BIDIRCPU": "Bidir CPU",
    "BIDIRVMCPU": "BidirVM CPU",
    "RTPATHOCL": "RT Path OpenCL",
    "RTPATHCPU": "RT Path CPU",
}

sampler_to_str = {
    "RANDOM": "Random",
    "SOBOL": "Sobol",
    "METROPOLIS": "Metropolis",
    "RTPATHCPUSAMPLER": "RT Path Sampler",
    "TILEPATHSAMPLER": "Tile Path Sampler"
}


def refresh(engine, scene, config, draw_film, time_until_film_refresh=0):
    """ Stats and optional film refresh during final render """
    engine._session.UpdateStats()
    stats = engine._session.GetStats()

    # Show stats string in UI
    pretty_stats = get_pretty_stats(config, stats)
    if draw_film:
        refresh_message = "Refreshing film..."
    else:
        refresh_message = "Film refresh in %ds" % time_until_film_refresh
    engine.update_stats(pretty_stats, refresh_message)

    if draw_film:
        # Show updated film
        engine._framebuffer.draw(engine, engine._session)

    return stats


def halt_condition_met(scene, stats):
    halt = scene.luxcore.halt

    if halt.enable:
        rendered_samples = stats.Get("stats.renderengine.pass").GetInt()
        rendered_time = stats.Get("stats.renderengine.time").GetFloat()

        if halt.use_time and (rendered_time > halt.time):
            print("Reached halt time: %d seconds" % halt.time)
            return True

        if halt.use_samples and (rendered_samples > halt.samples):
            print("Reached halt samples: %d samples" % halt.samples)
            return True

    return False


def get_pretty_stats(config, stats):
    pretty = []

    # Engine + Sampler
    engine = config.GetProperties().Get("renderengine.type").GetString()
    sampler = config.GetProperties().Get("sampler.type").GetString()
    pretty.append(engine_to_str[engine] + " + " + sampler_to_str[sampler])

    # Samples/Sec
    samples_per_sec = stats.Get("stats.renderengine.total.samplesec").GetFloat()

    if samples_per_sec > 10 ** 6 - 1:
        # Use megasamples as unit
        pretty.append("Samples/Sec %.1f M" % (samples_per_sec / 10 ** 6))
    else:
        # Use kilosamples as unit
        pretty.append("Samples/Sec %d k" % (samples_per_sec / 10 ** 3))

    return " | ".join(pretty)


def shortest_display_interval(scene):
    # Magic formula to compute shortest possible display interval (found through testing).
    # If the interval is any shorter, the CPU won't be able to keep up.
    # Only used for final renders.
    width, height = calc_filmsize(scene)
    return (width * height) / 852272.0 * 1.1
