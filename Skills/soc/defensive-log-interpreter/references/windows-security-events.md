# Windows Security Event Reference

Quick reference for interpreting Windows event logs. Event meaning is stable across modern Windows versions, but **which events are recorded depends on audit policy**, and some fields only appear when a specific subcategory or setting is enabled. When in doubt, verify against Microsoft's documentation for the OS version in question.

## Logon and session (Security log)
| ID | Meaning | Notes |
|---|---|---|
| 4624 | Successful logon | Read with Logon Type, Authentication Package, source address, Logon ID |
| 4625 | Failed logon | Read Status / Sub Status (below) |
| 4634 / 4647 | Logoff / user-initiated logoff | Join to 4624 on Logon ID for session length |
| 4648 | Logon with explicit credentials | e.g. `runas`, or a process supplying other credentials |
| 4672 | Special privileges assigned to new logon | Marks admin-equivalent sessions |
| 4740 / 4767 | Account locked out / unlocked | Check the PDC emulator DC, which processes lockouts domain-wide |

### Logon types (4624 / 4625)
| Type | Meaning |
|---|---|
| 2 | Interactive (console) |
| 3 | Network (SMB, many remote tools) |
| 4 | Batch (scheduled task) |
| 5 | Service |
| 7 | Unlock |
| 8 | Network cleartext (credentials sent in clear, e.g. IIS basic auth) |
| 9 | New credentials (`runas /netonly`) |
| 10 | Remote interactive (RDP) |
| 11 | Cached interactive (domain logon with cached credentials) |

### Status / sub-status codes (4625, 4776)
| Code | Meaning |
|---|---|
| 0xC000006A | Correct username, wrong password |
| 0xC0000064 | Username does not exist |
| 0xC000006D | Bad username or authentication information (generic) |
| 0xC000006F | Outside allowed logon hours |
| 0xC0000070 | Workstation restriction |
| 0xC0000071 | Password expired |
| 0xC0000072 | Account disabled |
| 0xC0000193 | Account expired |
| 0xC0000224 | Password must be changed at next logon |
| 0xC0000234 | Account locked out |
| 0xC000015B | Logon type not granted to this account |

## Kerberos and NTLM (domain controllers)
| ID | Meaning | Notes |
|---|---|---|
| 4768 | Kerberos TGT requested (AS-REQ) | Pre-Authentication Type 0 = no pre-auth; certificate fields populated = PKINIT (certificate logon) |
| 4769 | Kerberos service ticket requested (TGS-REQ) | Read Service Name, Ticket Encryption Type, client address |
| 4770 | Service ticket renewed | |
| 4771 | Kerberos pre-authentication failed | Failure code 0x18 = bad password |
| 4776 | NTLM credential validation | Recorded by the system that validated the account (DC for domain accounts) |

### Ticket encryption types (4768 / 4769)
| Value | Algorithm |
|---|---|
| 0x11 | AES128-CTS-HMAC-SHA1 |
| 0x12 | AES256-CTS-HMAC-SHA1 |
| 0x17 | RC4-HMAC |
| 0x18 | RC4-HMAC-EXP |
| 0x1 / 0x3 | DES (should not appear in modern domains) |

### Kerberos result / failure codes (4768, 4769, 4771)
| Code | Meaning |
|---|---|
| 0x6 | Client principal unknown (bad username) |
| 0x12 | Client credentials revoked (account disabled, expired or locked) |
| 0x17 | Password expired |
| 0x18 | Pre-authentication failed (bad password) |
| 0x25 | Clock skew too great |

Note: 0x17 means "RC4" in the *Ticket Encryption Type* field but "password expired" in the *Result/Failure Code* field. Always say which field a value came from.

## Account and group management
| ID | Meaning |
|---|---|
| 4720 / 4722 / 4725 / 4726 | User created / enabled / disabled / deleted |
| 4723 / 4724 | Password change attempt (by user) / password reset attempt (by someone else) |
| 4738 | User account changed (includes UAC flag changes) |
| 4728 / 4732 / 4756 | Member added to global / local / universal security group |
| 4729 / 4733 / 4757 | Member removed from global / local / universal security group |

## Directory service changes (DCs; require Directory Service auditing and SACLs)
| ID | Meaning | Notes |
|---|---|---|
| 4662 | Operation performed on an AD object | Properties field holds GUIDs of rights/attributes accessed |
| 5136 | Directory object modified | Shows attribute name and new value |
| 5137 / 5141 | Directory object created / deleted | |

## AD Certificate Services (on the CA; require CA auditing to be enabled)
| ID | Meaning |
|---|---|
| 4886 | Certificate request received |
| 4887 | Certificate request approved and issued |
| 4888 | Certificate request denied |
| 4899 | Certificate template updated |
| 4900 | Certificate template security updated |

## Process, services and scheduled tasks
| ID | Log | Meaning | Notes |
|---|---|---|---|
| 4688 / 4689 | Security | Process created / exited | Command line only if "Include command line in process creation events" is enabled |
| 4697 | Security | Service installed | |
| 7045 | System | Service installed | Recorded even when 4697 auditing is off |
| 4698 / 4699 / 4702 | Security | Scheduled task created / deleted / updated | |
| 106 | TaskScheduler/Operational | Task registered | |

## File shares
| ID | Meaning |
|---|---|
| 5140 | Network share accessed |
| 5145 | Detailed share access check (includes named pipes such as `\PIPE\...` over IPC$) |

## Logging and defence tampering
| ID | Log | Meaning |
|---|---|---|
| 1102 | Security | Security log cleared |
| 104 | System | Event log cleared (other logs) |
| 4719 | Security | System audit policy changed |
| 5001 | Microsoft Defender/Operational | Real-time protection disabled |
| 1116 / 1117 | Microsoft Defender/Operational | Malware detected / action taken |

## PowerShell and remote access
| ID | Log | Meaning |
|---|---|---|
| 4103 | PowerShell/Operational | Module logging (pipeline execution) |
| 4104 | PowerShell/Operational | Script block logging (de-obfuscated script text) |
| 1149 | TerminalServices-RemoteConnectionManager | RDP network authentication succeeded (not proof of a full logon) |
| 21 / 24 / 25 | TerminalServices-LocalSessionManager | RDP session logon / disconnect / reconnect |

## Sysmon (Microsoft-Windows-Sysmon/Operational)
| ID | Meaning |
|---|---|
| 1 | Process created (with hashes, parent, command line, OriginalFileName) |
| 2 | File creation time changed (possible timestomping) |
| 3 | Network connection |
| 5 | Process terminated |
| 6 | Driver loaded |
| 7 | Image (DLL) loaded |
| 8 | CreateRemoteThread |
| 10 | Process accessed (e.g. a handle to lsass.exe) |
| 11 | File created |
| 12 / 13 / 14 | Registry key/value created or deleted / value set / renamed |
| 15 | Alternate data stream created |
| 17 / 18 | Named pipe created / connected |
| 22 | DNS query |
| 23 / 26 | File deleted (archived) / file deletion detected |
| 25 | Process tampering (e.g. hollowing) |

Sysmon events only exist for what the deployed Sysmon configuration includes.
