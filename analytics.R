# ============================================================================
# Real Estate Marketplace - Advanced Analytics in R
# ============================================================================
# Author: Gabriel Demetrios Lafis
# Description: Comprehensive statistical analysis and data visualization for
#              real estate data with professional reporting capabilities
# Date: September 2025
# ============================================================================

# Load required libraries
library(ggplot2)
library(dplyr)
library(corrplot)
library(plotly)

# ============================================================================
# DataAnalyzer Reference Class
# ============================================================================
# Comprehensive data analysis class with methods for loading, analyzing,
# and generating professional reports from real estate data

DataAnalyzer <- setRefClass("DataAnalyzer",
  fields = list(
    data = "data.frame",
    results = "list",
    file_path = "character"
  ),
  
  methods = list(
    # ------------------------------------------------------------------------
    # Load Data Method
    # ------------------------------------------------------------------------
    # Loads CSV data file and performs initial validation
    # Parameters:
    #   file_path: Path to the CSV file
    # ------------------------------------------------------------------------
    load_data = function(file_path) {
      cat("\n=== Loading Data ===", "\n")
      tryCatch({
        data <<- read.csv(file_path, stringsAsFactors = FALSE)
        file_path <<- file_path
        cat("✓ Data loaded successfully\n")
        cat("  - Rows:", nrow(data), "\n")
        cat("  - Columns:", ncol(data), "\n")
        cat("  - File:", file_path, "\n")
        
        # Display column names
        cat("  - Variables:", paste(names(data), collapse=", "), "\n")
      }, error = function(e) {
        cat("✗ Error loading data:", conditionMessage(e), "\n")
      })
    },
    
    # ------------------------------------------------------------------------
    # Analyze Method
    # ------------------------------------------------------------------------
    # Performs comprehensive statistical analysis including:
    # - Descriptive statistics
    # - Correlation analysis
    # - Data visualizations
    # ------------------------------------------------------------------------
    analyze = function() {
      cat("\n=== Performing Analysis ===", "\n")
      
      if (nrow(data) == 0) {
        cat("✗ No data available for analysis\n")
        return()
      }
      
      # Descriptive statistics
      cat("\n1. Descriptive Statistics\n")
      summary_stats <- summary(data)
      print(summary_stats)
      
      # Correlation analysis for numeric variables
      numeric_cols <- sapply(data, is.numeric)
      if (sum(numeric_cols) > 1) {
        cat("\n2. Correlation Analysis\n")
        cor_matrix <- cor(data[, numeric_cols], use = "complete.obs")
        print(round(cor_matrix, 3))
        
        # Generate correlation plot
        tryCatch({
          corrplot(cor_matrix, method = "circle", type = "upper",
                   tl.col = "black", tl.srt = 45,
                   title = "Correlation Matrix - Real Estate Data")
        }, error = function(e) {
          cat("Note: Could not generate correlation plot\n")
        })
      }
      
      # Price distribution analysis (if price column exists)
      if ("price" %in% names(data)) {
        cat("\n3. Price Analysis\n")
        cat("  - Mean Price:", round(mean(data$price, na.rm = TRUE), 2), "\n")
        cat("  - Median Price:", round(median(data$price, na.rm = TRUE), 2), "\n")
        cat("  - Min Price:", round(min(data$price, na.rm = TRUE), 2), "\n")
        cat("  - Max Price:", round(max(data$price, na.rm = TRUE), 2), "\n")
      }
      
      # Visualization
      if (ncol(data) >= 2) {
        cat("\n4. Generating Visualizations\n")
        .self$generate_visualizations()
      }
      
      # Store results
      results <<- list(
        summary = summary_stats,
        correlation = if(exists("cor_matrix")) cor_matrix else NULL,
        timestamp = Sys.time()
      )
      
      cat("\n✓ Analysis completed successfully!\n")
    },
    
    # ------------------------------------------------------------------------
    # Generate Visualizations Method
    # ------------------------------------------------------------------------
    # Creates various plots for data visualization
    # ------------------------------------------------------------------------
    generate_visualizations = function() {
      # Price distribution histogram
      if ("price" %in% names(data)) {
        p1 <- ggplot(data, aes(x = price)) +
          geom_histogram(fill = "steelblue", color = "white", bins = 30) +
          theme_minimal() +
          labs(title = "Price Distribution",
               x = "Price", y = "Frequency") +
          theme(plot.title = element_text(hjust = 0.5, face = "bold"))
        print(p1)
      }
      
      # Property type distribution (if exists)
      if ("property_type" %in% names(data)) {
        p2 <- ggplot(data, aes(x = property_type)) +
          geom_bar(fill = "coral") +
          theme_minimal() +
          labs(title = "Property Types Distribution",
               x = "Property Type", y = "Count") +
          theme(plot.title = element_text(hjust = 0.5, face = "bold"),
                axis.text.x = element_text(angle = 45, hjust = 1))
        print(p2)
      }
      
      # Price by bedrooms (if both exist)
      if ("price" %in% names(data) && "bedrooms" %in% names(data)) {
        p3 <- ggplot(data, aes(x = factor(bedrooms), y = price)) +
          geom_boxplot(fill = "lightgreen") +
          theme_minimal() +
          labs(title = "Price by Number of Bedrooms",
               x = "Bedrooms", y = "Price") +
          theme(plot.title = element_text(hjust = 0.5, face = "bold"))
        print(p3)
      }
      
      # Scatter plot: square_feet vs price
      if ("price" %in% names(data) && "square_feet" %in% names(data)) {
        p4 <- ggplot(data, aes(x = square_feet, y = price)) +
          geom_point(alpha = 0.6, color = "darkblue") +
          geom_smooth(method = "lm", color = "red", se = TRUE) +
          theme_minimal() +
          labs(title = "Price vs Square Footage",
               x = "Square Feet", y = "Price") +
          theme(plot.title = element_text(hjust = 0.5, face = "bold"))
        print(p4)
      }
    },
    
    # ------------------------------------------------------------------------
    # Generate Report Method
    # ------------------------------------------------------------------------
    # Generates a professional analysis report
    # Parameters:
    #   output_dir: Directory to save report files (default: data/reports)
    # ------------------------------------------------------------------------
    generate_report = function(output_dir = "data/reports") {
      cat("\n=== Generating Analytics Report ===", "\n")
      
      # Ensure output directory exists
      if (!dir.exists(output_dir)) {
        dir.create(output_dir, recursive = TRUE)
        cat("✓ Created output directory:", output_dir, "\n")
      }
      
      # Report header
      cat("\n┌", paste(rep("─", 60), collapse=""), "┐\n")
      cat("│", sprintf("%-58s", "  REAL ESTATE ANALYTICS REPORT"), "│\n")
      cat("└", paste(rep("─", 60), collapse=""), "┘\n")
      
      cat("\nReport Details:\n")
      cat("  • Generated:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")
      cat("  • Data Source:", file_path, "\n")
      cat("  • Dataset Size:", nrow(data), "rows ×", ncol(data), "columns\n")
      
      # Data quality metrics
      cat("\nData Quality:\n")
      missing_counts <- colSums(is.na(data))
      if (sum(missing_counts) > 0) {
        cat("  • Missing Values Detected:\n")
        for (col in names(missing_counts[missing_counts > 0])) {
          cat("    -", col, ":", missing_counts[col], "missing\n")
        }
      } else {
        cat("  • No missing values detected\n")
      }
      
      # Key insights
      cat("\nKey Insights:\n")
      if ("price" %in% names(data)) {
        cat("  • Average Property Price:", 
            format(mean(data$price, na.rm = TRUE), big.mark=",", scientific=FALSE), "\n")
      }
      if ("property_type" %in% names(data)) {
        type_counts <- table(data$property_type)
        cat("  • Most Common Property Type:", 
            names(which.max(type_counts)), 
            "(", max(type_counts), "properties)\n")
      }
      
      cat("\n✓ Report generated successfully!\n")
      cat("  Output directory:", output_dir, "\n")
    }
  )
)

# ============================================================================
# Module Initialization
# ============================================================================
cat("\n═══════════════════════════════════════════════════════════════\n")
cat("  Real Estate Analytics Module (R)\n")
cat("  Author: Gabriel Demetrios Lafis\n")
cat("═══════════════════════════════════════════════════════════════\n")

cat("\n✓ Module loaded successfully!\n")
cat("\nUsage Instructions:\n")
cat("  1. Create analyzer instance:\n")
cat("     analyzer <- DataAnalyzer$new()\n\n")
cat("  2. Load data:\n")
cat("     analyzer$load_data('data/sample.csv')\n\n")
cat("  3. Perform analysis:\n")
cat("     analyzer$analyze()\n\n")
cat("  4. Generate report:\n")
cat("     analyzer$generate_report(output_dir='data/reports')\n\n")
cat("═══════════════════════════════════════════════════════════════\n")
