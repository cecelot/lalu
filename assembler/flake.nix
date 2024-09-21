{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem
    (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.default = let
        python-pkgs = p:
          with p; [
            cryptography
          ];
      in
        pkgs.mkShell {
          buildInputs = with pkgs; [
            (python3.withPackages python-pkgs)
          ];
        };
    });
}
