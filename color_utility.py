import colorsys

def phue_set_color(R, G, B, address, light_num):
    import phue
    bridge = phue.Bridge(address) 
    h, s, v = colorsys.rgb_to_hsv(R, G, B)
    bridge.set_light(light_num, 'hue', int(round(h * 65535)))
    bridge.set_light(light_num, 'sat', int(round(s * 255)))
    bridge.set_light(light_num, 'bri', int(round(v)))