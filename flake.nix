{
  description = "A tool for running restic backups";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.03";
  inputs.dirstamp.url = "github:orangeturtle739/dirstamp";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, dirstamp, flake-utils }:
    flake-utils.lib.eachSystem
    (flake-utils.lib.defaultSystems ++ [ "armv7l-linux" ]) (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pydeps = with pkgs.python3Packages; [ setuptools click ];
        pybuilddeps = with pkgs.python3Packages; [
          black
          flake8
          isort
          mypy
          wrapPython
        ];
        mypy_hook = pkgs.makeSetupHook { } (pkgs.writeScript "mypy_hook" ''
          export MYPYPATH=$(toPythonPath "${
            builtins.concatStringsSep " " pydeps
          }")
        '');
        jgrestic = pkgs.stdenv.mkDerivation rec {
          pname = "jgrestic";
          version = pkgs.lib.removeSuffix "\n" (builtins.readFile ./VERSION);
          src = self;
          nativeBuildInputs = pybuilddeps ++ [
            pkgs.cmake
            pkgs.ensureNewerSourcesForZipFilesHook
            pkgs.restic
            dirstamp.defaultPackage.${system}
          ];
          buildInputs = [ mypy_hook ];
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
