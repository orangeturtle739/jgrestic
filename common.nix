{ jgresticsrc, python3Packages, runCommand, restic }:
let
  gen-package = { name, text }:
    let
      pysrc = runCommand "${name}-gen-package" {
        inherit text;
        passAsFile = [ "text" ];
        preferLocalBuild = true;
        allowSubstitutes = false;
      } ''
        mkdir $out
        pushd $out
        cat << EOF > setup.py
        from setuptools import setup, find_packages
        packages = find_packages()
        setup(
            name="${name}",
            packages=packages,
            package_data={pkg: ["py.typed"] for pkg in packages},
        )
        EOF
        mkdir ${name}
        cp -a "$textPath" "${name}/__init__.py"
        touch "${name}/py.typed"
        popd
      '';
    in python3Packages.buildPythonPackage rec {
      inherit name;
      src = "${pysrc}";
    };

  jgrestic-deps = gen-package {
    name = "jgrestic_deps";
    text = ''
      restic = "${restic}"
    '';
  };

  pydeps = with python3Packages; [ toml jgrestic-deps ];
in python3Packages.buildPythonPackage rec {
  name = "jgrestic";
  src = jgresticsrc;
  nativeBuildInputs = with python3Packages; [ black flake8 mypy ];
  propagatedBuildInputs = pydeps;
  postShellHook = ''
    export MYPYPATH=$(toPythonPath "${builtins.concatStringsSep " " pydeps}")
  '';
}
