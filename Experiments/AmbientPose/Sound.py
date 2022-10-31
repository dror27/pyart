# generate scale
import musthe
import pyo
import time


# list all scales
def all_scales():
    return list(dict.fromkeys([s.name for s in musthe.Scale.all(include_greek_modes=True)]))

# generate a multi octave scale
def multi_octave_scale(note, name, octaves):
    #print("note: %s, name: %s, octaves: %d" % (note, name, octaves))
    if octaves == 0:
        return [note]
    else:
        s = musthe.Scale(note, name)
        return [s[i] for i in range(len(s))] + multi_octave_scale(note + musthe.Interval('P8'), name, octaves - 1)

# start sound engine
def start(args):

    # save args need
    global add_beat
    add_beat = args.add_beat

    # some global setup
    global s, osc4, osc5, scale1, scale2, beat, beat_id, beat_pattern, sf, pat
    global t, tr2, lfo4, lfo5
    scale1 = multi_octave_scale(musthe.Note(args.note_left), args.scale, 2)
    scale2 = multi_octave_scale(musthe.Note(args.note_right), args.scale, 2)
    beat_id = 1
    beat_pattern = args.beat_pattern
    beat_time = 60.0 / args.bpm / 4
    print("beat_time: %f\n" % beat_time)

    # start sound engine
    s = pyo.Server().boot()
    t = pyo.CosTable([(0,0), (100,1), (500,.3), (8191,0)])
    beat = pyo.Beat(time=beat_time, taps=16, w1=[90,80], w2=50, w3=35, poly=1).play()
    tr2 = pyo.TrigEnv(beat, table=t, dur=beat['dur'], mul=beat['amp'])

    lfo4 = pyo.Sine(0.1).range(0.1, 0.75)
    osc4 = pyo.SuperSaw(freq=scale1[0].frequency(), detune=lfo4, mul=tr2).out(1)
    lfo5 = pyo.Sine(0.1888).range(0.1, 0.75)
    osc5 = pyo.SuperSaw(freq=scale2[0].frequency(), detune=lfo5, mul=tr2).out(2)
    sf = pyo.SfPlayer("kick-02.wav", speed=1, loop=False, mul=0.5).out()
    pat = pyo.Pattern(function=beat_event, time=beat_time).play()

    s.start()

def stop():

    global s, osc4, osc5, scale1, scale2, beat, beat_id, beat_factor, sf, pat
    global t, tr2, lfo4, lfo5

    beat.stop()
    tr2.stop()
    lfo4.stop()
    lfo5.stop()

    osc4.stop()
    osc5.stop()
    pat.stop()
    sf.stop()

    s.stop()

    print("Sound stopped")
    time.sleep(1)



def beat_event():
    global beat_id, beat_factor, sf

    if add_beat and ((1 << (beat_id & 0xF)) & beat_pattern) != 0:
        sf.out()
    beat_id = beat_id + 1

# define motion processors
def y_note(y, scale):
    y = min(1.0, max(0.0, y))
    return scale[int((1 - y) * (len(scale) - 1))]







