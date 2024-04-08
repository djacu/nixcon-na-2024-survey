{
  description = "NixCon NA 2024 Survey Processing";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
    poetry2nix.inputs.flake-utils.follows = "flake-utils";
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    flake-utils.lib.eachSystem ["x86_64-linux"] (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      lib = pkgs.lib;
      inherit (lib) fileset;
      inherit
        (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;})
        mkPoetryEnv
        ;

      processing = mkPoetryEnv {
        preferWheels = true;
        projectDir = fileset.toSource {
          root = ./.;
          fileset = fileset.unions [
            ./pyproject.toml
            ./poetry.lock
          ];
        };
        python = pkgs.python311;
      };
    in {
      devShells = {
        poetry = pkgs.mkShell {
          packages = [
            pkgs.poetry
            pkgs.python311
          ];
        };
        nnasp = pkgs.mkShell {
          buildInputs = [
            pkgs.poetry
            processing
          ];
        };
      };
    });
}
