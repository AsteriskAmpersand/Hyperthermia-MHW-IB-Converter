<p align="center">
  <img src="https://cdn.discordapp.com/attachments/648568315937161233/669828862791647242/HyperthermiaLogo.fw.png">
</p>

## Hyperthemia: A Base Game MHW to Iceborne Asset Converter
Hyperthermia is an open source converter for MHW base game files into MHW:Iceborne format. This tool is intended as a modder's resource for quickly updating simple visual mods and helping with the updating process.

It comes with a CLI and a GUI release. The GUI operates on the CLI code on the backend however so the behaviours are identical.

### Credits
#### Author
* **AsteriskAmpersand/\*&**

#### Acknowledgements
* **CrazyT** - For his research into the mrl3 file format, almost the entire structure is known thanks to him. Additionaly his shader research is to credit for the labelling of the parameter sections. - [CrazyT's Github User Page](https://github.com/TheCrazyT)
* **DMQW - Ice** - For the research into the ctc changes.
* **Statyk** - For his research into the ctc and ccl changes.
* **Silvris** - For his assistance with comparison between specific files and QA.
* **Nack, asdasdasdasd, LyraVeil** - For help with testing.

### Technical Background
Hyperthermia works on each file format in different ways:
#### MRL3
It compares the shader hash (which is untouched) between each material in the supplied mrl3 and a master list. When the matching hash is found it creates an mrl3 from the new material in the master list but updates all of its properties to match that of the supplied mrl3. All of the resource bindings are sequentially compared. Resource Bindings that existed before are pointed to the resources of the mrl3 being converted. All of the parameter arrays are compared, when they match the values of the supplied mrl3 are taken, those that didn't exist are defaulted to those of the master list. If the parameter arrays have data type mismatches types are coerced within bounds of reason (smaller arrays are coerced by appending 0s for example).
#### CCL
The format has minor changes. When a null value is present on certain positions it's replaced by -51,

#### CTC
The header is updated to match Iceborne's new headers. A section with boilerplate constant is added to every record.

#### EVXX
Because of the lack of research into the format this files are heurstically matched. The user is given the option of overriding the heuristic with a default (for body it's pl001, for weapons it's the evwp of the first weapon model on the weapon's class) or a premade file (hollow head or untouched head for evhl). The heuristic does binary comparisons of the evxx file against all evxx files in the base game version, if a match is found the equivalent evxx is loaded from the iceborne files and used instead. If the heuristic fails then it falls back to a default value.

#### WP_DAT
Matches the entry indices between the base game wp_dat and the iceborne wp_dat. Uses this mapping to transpose player edits of visual fields to the iceborne wp_dat.
