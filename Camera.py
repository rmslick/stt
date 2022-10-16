from math import pi, atan, sqrt
class Camera:
    QE = 0.6 # Quantum Efficiency
    Int = 0.1 # [sec]
    A = (pi*0.016^2)/4 # [m^2]
    Nsize = 25 # [pixels] Individual Star Block Size: 25x25
    pp = 2.5e-6 # [m] Pixel Pitch
    f = 0.016 # [m] Focal Length
    U = 2000 # [pixels] Number of pixels vertically
    V = 1000 # [pixels] Number of pixels in horizontally
    FOVx = 2*atan((V*pp/(2*f)))
    #[rad] Horizontal Field of View
    FOVy = 2*atan((U*pp)/(2*f))
    #[rad] Vertical Field of View
    FOV = sqrt(FOVx^2 + FOVy^2)/2
    #[rad] Diagonal Field of View
    sigma = 2
    #standard deviation, how much the star spreads over pixels
    QSE = 7.3
    #Quantum Step Equivalence = full well capacity/dynamic range
    bits = 12 # Bit size
    DG = 10 # Digital Gain scale factor