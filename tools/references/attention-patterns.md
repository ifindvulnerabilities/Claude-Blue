# Command-Line Attention Patterns

Patterns that deserve a closer look in process and command-line telemetry. **None of these is proof of malice on its own.** Each row lists common legitimate contexts so the analyst can weigh both readings. ATT&CK IDs are indicative mappings, not verdicts.

## Execution options that hide or loosen controls
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `-WindowStyle Hidden`, `-w hidden` | Hides the console from the user | Login scripts, RMM agents, installers | T1564.003 |
| `-NoProfile`, `-nop` | Skips profile scripts | Very common in automation | — |
| `-ExecutionPolicy Bypass`, `-ep bypass` | Ignores script policy | Software deployment, IT scripts | T1059.001 |
| `-EncodedCommand`, `-enc`, `-e` | Base64 (UTF-16LE) payload hides intent | Some management tools encode to avoid quoting issues | T1027 |
| Caret, backtick, quote or `+` string splitting | Obfuscation to defeat string matching | Rarely legitimate | T1027 |

## Download and staging
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `Invoke-WebRequest`/`IWR`, `Net.WebClient`, `Start-BitsTransfer` | Retrieves content from a URL | Installers, update scripts | T1105 |
| `IEX`/`Invoke-Expression` on downloaded content | Runs fetched code directly in memory | Rare in legitimate admin work | T1059.001 |
| `certutil -urlcache -f`, `certutil -decode` | Built-in tool used to download or decode | Certificate management (urlcache rarely) | T1105, T1140 |
| `bitsadmin /transfer` | Background download | Legacy deployment scripts | T1197 |
| `curl`/`wget` piped to `sh`/`bash` | Fetch-and-run | Some vendor install one-liners | T1105, T1059.004 |
| `base64 -d \| sh` | Decode-and-run | Rare | T1140 |

## Signed binary proxy execution (LOLBins)
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `mshta` with a URL or inline script | Runs HTA/script content | Very rare today | T1218.005 |
| `rundll32` with unusual DLL path, URL, or `javascript:` | Proxy execution of code | Many legitimate DLL entry points (check the path and export) | T1218.011 |
| `regsvr32 /s /n /u /i:<url> scrobj.dll` | Remote scriptlet execution | Very rare | T1218.010 |
| `msiexec /q /i http…` | Silent install from a URL | Software deployment from internal servers | T1218.007 |
| `wmic process call create` | Spawns a process via WMI | Admin tooling (wmic is deprecated) | T1047 |

## Discovery
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `whoami /all`, `net group "domain admins" /domain`, `nltest /dclist:` | Enumerates privileges, admins, DCs | Helpdesk troubleshooting, admin scripts | T1033, T1069, T1018 |
| Bursts of `systeminfo`, `ipconfig /all`, `net view`, `arp -a` | Typical early reconnaissance sequence | Individually common; the burst is the signal | T1082, T1016, T1135 |

## Remote execution and lateral movement
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `psexec`/`PSEXESVC` service creation | Remote service execution | Admin tooling | T1569.002 |
| `wmic /node:`, `Invoke-Command -ComputerName`, `winrs` | Remote command execution | Admin and deployment tooling | T1047, T1021.006 |
| `schtasks /create /s <remote host>` | Remote scheduled task | Rare outside deployment tools | T1053.005 |

## Persistence
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `schtasks /create`, `sc create`, `New-Service` | Survives reboot | Installers, agents | T1053.005, T1543.003 |
| `reg add …\CurrentVersion\Run` | Runs at logon | Many applications | T1547.001 |
| New cron entries, systemd units, `~/.bashrc` / `~/.profile` edits | Linux persistence | Admin configuration management | T1053.003, T1543.002, T1546.004 |

## Credential access
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `comsvcs.dll` `MiniDump` targeting lsass | Dumps credentials from memory | Essentially never | T1003.001 |
| `procdump -ma lsass` | Dumps lsass memory | Rare; some vendor support cases | T1003.001 |
| `reg save HKLM\SAM` / `HKLM\SYSTEM` / `HKLM\SECURITY` | Copies local credential hives | Rare; some backup tools | T1003.002 |
| `ntdsutil` with `ifm` | Copies the AD database | DC backup or promotion media | T1003.003 |

## Defence impairment and recovery inhibition
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `Set-MpPreference -Disable…`, `Add-MpPreference -ExclusionPath` | Weakens Defender | Exclusions added by IT for line-of-business apps | T1562.001 |
| `wevtutil cl`, `Clear-EventLog`, `auditpol /clear` | Removes or stops logging | Very rare | T1070.001, T1562.002 |
| `vssadmin delete shadows`, `wmic shadowcopy delete` | Deletes shadow copies | Rare; disk-space cleanup | T1490 |
| `wbadmin delete catalog`, `bcdedit /set … recoveryenabled no` | Disables recovery | Rare | T1490 |

## Collection and exfiltration
| Pattern | Why it draws attention | Often legitimate when | ATT&CK |
|---|---|---|---|
| `7z`/`rar` with a password flag (`-p`, `-hp`) on large sets of files | Staged, encrypted archive | Users archiving their own files | T1560.001 |
| `rclone` to a cloud remote | Bulk upload to cloud storage | Backup jobs | T1567.002 |

Sources: MITRE ATT&CK (attack.mitre.org), LOLBAS (lolbas-project.github.io), GTFOBins (gtfobins.github.io).
