{
  description = "A tool for running restic backups";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.05";
  inputs.dirstamp = {
    url = "github:orangeturtle739/dirstamp";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  inputs.flake-utils = {
    url = "github:numtide/flake-utils";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  inputs.unicmake = {
    url = "github:orangeturtle739/unicmake";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  # inputs.unicmake.url = "/home/jacob/Documents/MyStuff/projects/unicmake";

  outputs = { self, nixpkgs, dirstamp, flake-utils, unicmake }:
    flake-utils.lib.eachSystem [ "aarch64-linux" "i686-linux" "x86_64-linux" ]
    (system:
      let
        pkgs = import nixpkgs { inherit system; };
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
            dirstamp.defaultPackage.${system}
          ];
          buildInputs = [ unicmake.defaultPackage.${system} ];
          propagatedBuildInputs = pydeps;
          postFixup = ''
            wrapPythonPrograms
              '';
        };
      in {
        devShell = jgrestic;
        defaultPackage = jgrestic;
      });
}
