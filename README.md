# WeeChat

**WeeChat** is a fast, light and extensible chat client, with a text-based user interface.

WeeChat is:

- Modular: a lightweight core with optional plugins.
- Multi-protocols architecture (mainly IRC).
- Multi-platforms: Linux, Unix, BSD, GNU Hurd, Haiku, macOS and Windows (Bash/Ubuntu and Cygwin).
- Extensible with C, Python, Perl, Ruby, Lua, Tcl, Scheme, Javascript and PHP.
- Fully documented and translated into several languages.
- A free program released under the terms of the GNU General Public License version 3.
- An active project with a large community for scripts.

## Install

### Fedora COPR

```
$ dnf copr enable pkgstore/weechat
$ dnf install -y weechat
```

### Open Build Service (OBS)

```
# Work in Progress
```

## Update

```
$ dnf upgrade -y weechat
```

## Remove

```
$ dnf erase -y weechat
$ dnf copr remove pkgstore/weechat
```

## How to Build

1. Get source from [src.fedoraproject.org](https://src.fedoraproject.org/rpms/weechat).
2. Write last commit SHA from [src.fedoraproject.org](https://src.fedoraproject.org/rpms/weechat) to [CHANGELOG](CHANGELOG).
3. Modify & update source (and `*.spec`).
4. Build SRPM & RPM.
