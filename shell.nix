{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "pygame-numpy-env";

  buildInputs = [
    pkgs.python312         
    pkgs.python312Packages.pygame
    pkgs.python312Packages.numpy
  ];

  shellHook = ''
    echo "Python with pygame and numpy is ready!"
  '';
}
