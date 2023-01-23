{
  description = "A tool for running restic backups";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
  inputs.dirstamp = {
    url = "github:orangeturtle739/dirstamp";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  inputs.flake-utils = { url = "github:numtide/flake-utils"; };
  inputs.unicmake = {
    url = "github:orangeturtle739/unicmake";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  # inputs.unicmake.url = "/home/jacob/Documents/MyStuff/projects/unicmake";

  outputs = { self, nixpkgs, dirstamp, flake-utils, unicmake }:
    let
      withPkgs = base:
        let
          pkgs = (base.extend unicmake.overlays.default).extend
            dirstamp.overlays.default;
          pydeps = with pkgs.python3Packages; [ setuptools click ];
          pybuilddeps = with pkgs.python3Packages; [
            black
            flake8
            isort
            mypy
            wrapPython
            pytest
          ];
          jgrestic = pkgs.stdenv.mkDerivation rec {
            pname = "jgrestic";
            version =
              "0.2.2"; # pkgs.lib.removeSuffix "\n" (builtins.readFile ./VERSION);
            src = self;
            nativeBuildInputs = pybuilddeps ++ [
              pkgs.cmake
              pkgs.ensureNewerSourcesForZipFilesHook
              pkgs.restic
              pkgs.dirstamp
            ];
            buildInputs = [ pkgs.unicmake ];
            propagatedBuildInputs = pydeps;
            postFixup = ''
              wrapPythonPrograms
            '';
          };
        in {
          devShells.default = jgrestic;
          packages.default = jgrestic;
        };
    in (flake-utils.lib.eachSystem [
      "aarch64-linux"
      "i686-linux"
      "x86_64-linux"
    ] (system: withPkgs (import nixpkgs { inherit system; }))) // {
      overlays.default = final: prev: {
        jgrestic = (withPkgs prev).packages.default;
      };
    };
}
