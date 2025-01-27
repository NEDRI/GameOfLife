{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "pygame-numpy-env";

  buildInputs = [
    pkgs.python311         
    pkgs.python311Packages.pygame
    pkgs.python311Packages.numpy
  ];

  shellHook = ''
    echo "Python with pygame and numpy is ready!"
  '';
}
