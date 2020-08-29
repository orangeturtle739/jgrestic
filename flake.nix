{
  description = "A tool for running restic backups";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.03";
  inputs.dirstamp.url = "github:orangeturtle739/dirstamp";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, dirstamp, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pydeps = with pkgs.python3Packages; [ toml setuptools click ];
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
          version = "0.1.0";
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
