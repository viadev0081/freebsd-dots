// wave.frag
#ifdef GL_ES
precision mediump float;
#endif

uniform float time;
uniform vec2 resolution;
uniform sampler2D tex;

varying vec2 v_texcoord;

void main() {
    vec2 uv = v_texcoord;
    float wave = sin(uv.y * 25.5 + time * 5.5) * 0.02;
    uv.x += wave;
    vec4 color = texture2D(tex, uv);
    gl_FragColor = color;
}

