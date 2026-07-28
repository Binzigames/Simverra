#version 330

in vec2 fragTexCoord;
in vec4 fragColor;

uniform sampler2D texture0;
uniform float time;

out vec4 finalColor;


// Fantasy soft bloom
vec3 bloom(vec2 uv)
{
    vec3 result = vec3(0.0);

    vec2 pixel = vec2(1.0) / 800.0;

    for(int x=-2;x<=2;x++)
    {
        for(int y=-2;y<=2;y++)
        {
            vec3 sample =
            texture(
                texture0,
                uv + vec2(x,y)*pixel*3.0
            ).rgb;


            float light =
            max(max(sample.r,sample.g),sample.b);


            // тільки яскраві магічні джерела
            result += sample *
            smoothstep(0.75,1.4,light);
        }
    }

    return result / 25.0 * 0.45;
}



void main()
{
    vec2 uv = fragTexCoord;


    vec3 color =
    texture(texture0,uv).rgb;



    //==================
    // Magical bloom
    //==================

    color += bloom(uv);



    //==================
    // Fantasy color grading
    //==================

    // тепле світло
    color.r *= 1.06;

    // трохи магічного фіолетового
    color.b *= 1.04;


    // більше кольору
    float luminance =
    dot(color,vec3(
        0.299,
        0.587,
        0.114
    ));

    color =
    mix(
        vec3(luminance),
        color,
        1.15
    );



    //==================
    // Very soft vignette
    //==================

    vec2 center = uv - 0.5;

    float vignette =
    1.0 - dot(center,center)*0.35;

    color *= vignette;



    //==================
    // Magical glow curve
    //==================

    color =
    pow(color,vec3(0.92));



    //==================
    // Tiny film grain
    //==================

    float noise =
    fract(
        sin(dot(
            uv*time,
            vec2(12.9898,78.233)
        ))
        *43758.5453
    );

    color += noise*0.004;



    finalColor =
    vec4(color,1.0);
}