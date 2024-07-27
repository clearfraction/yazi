Name:           yazi
Version:        %(unset https_proxy && curl -s https://api.github.com/repos/sxyazi/yazi/releases/latest | grep -oP '"tag_name": "v\K(.*)(?=")')
Release:        1
URL:            https://github.com/sxyazi/yazi
Source0:        https://github.com/sxyazi/yazi/archive/refs/tags/v%{version}.tar.gz
Summary:        Blazing fast terminal file manager written in Rust, based on async I/O
License:        MIT
BuildRequires :  rustc ImageMagick


%description
Yazi (means "duck") is a terminal file manager written in Rust, based on non-blocking async I/O. It aims to provide an efficient, user-friendly, and customizable file management experience.


%prep
%setup -q -n yazi-%{version}


%build
unset https_proxy http_proxy
export RUSTFLAGS="$RUSTFLAGS -C target-cpu=westmere -C target-feature=+avx,+fma,+avx2 -C opt-level=3 -C codegen-units=1 -C panic=abort -Clink-arg=-Wl,-z,now,-z,relro,-z,max-page-size=0x4000,-z,separate-code  "
export YAZI_GEN_COMPLETIONS=true
export VERGEN_GIT_SHA="Clear Linux"
cargo build --release
strip target/release/yazi


%install
install -Dm755 target/release/yazi %{buildroot}/usr/bin/yazi
install -Dm644 assets/yazi.desktop %{buildroot}/usr/share/applications/yazi.desktop
install -dm0755 %{buildroot}/usr/share/icons/hicolor/128x128/apps
convert assets/logo.png -resize 128x128 %{buildroot}/usr/share/icons/hicolor/128x128/apps/yazi.png

install -Dm644 yazi-boot/completions/yazi.bash %{buildroot}/usr/share/bash-completion/completions/yazi
install -Dm644 yazi-boot/completions/yazi.fish -t %{buildroot}/usr/share/fish/vendor_completions.d/
install -Dm644 yazi-boot/completions/_yazi -t %{buildroot}/usr/share/zsh/site-functions/


%files
%defattr(-,root,root,-)
/usr/bin/yazi
/usr/share/applications/yazi.desktop
/usr/share/icons/hicolor/128x128/apps/yazi.png
/usr/share/bash-completion/completions/yazi
/usr/share/fish/vendor_completions.d/yazi.fish
/usr/share/zsh/site-functions/_yazi
