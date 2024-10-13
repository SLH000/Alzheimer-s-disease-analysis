install.packages("openxlsx")
install.packages("tidyverse")
library("tidyverse")
library(openxlsx)
library(dplyr)
adCT <- read.xlsx("merged_output.xlsx", sheet = 1)
adCT_tibble <- as.tibble(adCT)

# Filter for rows where Phase is "PHASE3"
phase3_data <- adCT_tibble %>% filter(Phases == "PHASE3")

summary(adCT_tibble)

# Analyze Funder
funder_count <- adCT_tibble %>%
  group_by(Funder.Type) %>%
  summarize(Count = n(), .groups = 'drop')
# Plot the bar chart
fundPlot <- ggplot(funder_count, aes(x = Funder.Type, y = Count, fill = Funder.Type)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(title = "Distribution of Funder Types in AD Clinical Trials", 
       x = "Funder Type", 
       y = "Number of Trials") + theme(
         axis.text.x = element_text(size = 10,  # Font size
                                    angle = 45,  # Angle of text
                                    hjust = 1,   # Horizontal justification
                                    vjust = 1,   # Vertical justification
                                    face = "plain",  # Font face: "plain", "italic", "bold", "bold.italic"
                                    color = "black")) # Font color

# Analyze Phase 
phase_count <- adCT_tibble %>%
  group_by(Phases) %>%
  summarize(Count = n(), .groups = 'drop')

cphase_count <- phase_count %>%
  filter(!is.na(Phases) & Phases != "NA")


phasePlot <- ggplot(cphase_count, aes(x = Phases, y = Count, fill = Phases)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(title = "Distribution of Funder Types in AD Clinical Trials", 
       x = "Phases", 
       y = "Number of Trials") + theme(
         axis.text.x = element_text(size = 10,  # Font size
                                    angle = 45,  # Angle of text
                                    hjust = 1,   # Horizontal justification
                                    vjust = 1,   # Vertical justification
                                    face = "plain",  # Font face: "plain", "italic", "bold", "bold.italic"
                                    color = "black")) # Font color

# Analyze Status 
status_count <- adCT_tibble %>%
  group_by(Study.Status) %>%
  summarize(Count = n(), .groups = 'drop')
cstatus_count <- status_count %>%
  filter(!is.na(Study.Status) & Study.Status != "NA")

statusPlot <- ggplot(cstatus_count, aes(x = Study.Status, y = Count, fill = Study.Status)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(title = "Distribution of Funder Types in AD Clinical Trials", 
       x = "Phases", 
       y = "Number of Trials") + theme(
         axis.text.x = element_text(size = 10,  # Font size
                                    angle = 45,  # Angle of text
                                    hjust = 1,   # Horizontal justification
                                    vjust = 1,   # Vertical justification
                                    face = "plain",  # Font face: "plain", "italic", "bold", "bold.italic"
                                    color = "black")) # Font color

# Convert Completion.Date to Date object
adCT_tibble <- adCT_tibble %>%
  mutate(Completion.Date = as.Date(Completion.Date, format = "%Y-%m-%d"))

# Extract year from Completion.Date
adCT_tibble <- adCT_tibble %>%
  mutate(Year = year(Completion.Date))

# Count number of entries per year
yearly_counts <- adCT_tibble %>%
  count(Year)
# Filter for years 2020 to 2030
filtered_counts <- yearly_counts %>%
  filter(Year >= 2020 & Year <= 2030)
# Plot the bar chart
ggplot(filtered_counts , aes(x = Year, y = n)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  labs(title = "Number of Studies Completed by Year", x = "Year", y = "Count") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Remove rows where Phases is NA
cleaned_adCT_tibble <- adCT_tibble %>%
  drop_na(Phases, pi, Interventions)  

# Filter for studies ending in 2024 and 2025
filtered_data <- cleaned_adCT_tibble %>%
  filter(Year %in% c(2024, 2025, 2026, 2027), Funder.Type == "INDUSTRY")

resultTable <- filtered_data %>% select(nct_id, Study.Status, Interventions, Primary.Outcome.Measures, 
                                      Secondary.Outcome.Measures, Sponsor, Phases, Start.Date, Primary.Completion.Date)
write.csv(resultTable, file = "resultTable.csv", row.names = FALSE)

