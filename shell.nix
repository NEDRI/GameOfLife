{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "pygame-numpy-env";

  buildInputs = [
    pkgs.python311         # Use Python 3.11 or your preferred version
    pkgs.python311Packages.pygame
    pkgs.python311Packages.numpy
  ];

  shellHook = ''
    echo "Python with pygame and numpy is ready!"
  '';
}
