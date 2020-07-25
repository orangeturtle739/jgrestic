let
  pkgs = import <nixpkgs> { };
  jgpkgs = import (pkgs.fetchFromGitHub {
    owner = "orangeturtle739";
    repo = "nix-packages";
    rev = "64eded6e16f19a6ed210fdce4a2f8901791df148";
    sha256 = "14ksy685xkq7an1bprl812y747m5b6plvm9c2pbgic7d6hh9h26c";
  }) { inherit pkgs; };
  pydeps = with pkgs.python3Packages; [ toml ];
  pybuilddeps = with pkgs.python3Packages; [ black flake8 isort mypy ];
in pkgs.stdenv.mkDerivation rec {
  name = "jgrestic";
  nativeBuildInputs = with pkgs;
    pybuilddeps
    ++ [ cmake ensureNewerSourcesForZipFilesHook restic jgpkgs.dirstamp ];
  propagatedBuildInputs = pydeps;
  shellHook = ''
    export MYPYPATH=$(toPythonPath "${builtins.concatStringsSep " " pydeps}")
  '';
}
