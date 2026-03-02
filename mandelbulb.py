// mandelbulb

double mandelbulb(double x0, double y0, double z0) {
  double x = x0;
  double y = y0;
  double z = z0;
  double r2, theta, phi, r6, r8;
  double dr = 1.0;
  for(int i = 0; i < 24; i++) {
    r2 = x * x + y * y + z * z;
    if(r2 > 4) {
      return 0.25 * sqrt(r2) * log(r2) / dr;
    }
    r6 = r2 * r2 * r2;
    dr = 8.0 * r6 * sqrt(r2) * dr + 1.0;
    theta = 8.0 * atan2(sqrt(x * x + y * y), z);
    phi = 8.0 * atan2(y, x);
    r8 = r6 * r2;
    x = r8 * cos(phi) * sin(theta) + x0;
    y = r8 * sin(phi) * sin(theta) + y0;
    z = r8 * cos(theta) + z0;
  }
  return 0.0;
}
